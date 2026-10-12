#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quay video từ một web app bằng Chrome DevTools Protocol (CDP) trên Xvfb, không cần màn hình thật.

ĐÂY LÀ PHẦN GENERIC, đã chạy thật trong một dự án (video 4:33 nộp hồ sơ dự thi). Phần riêng của dự
án (bấm nút nào, framing ra sao) là việc của caller — xem hàm `actions` trong `record_shot`.

VÌ SAO DÙNG CDP SCREENCAST CHỨ KHÔNG PHẢI ffmpeg x11grab.
`x11grab` chụp TOÀN BỘ màn hình X. Trên Xvfb không có window manager, Chrome tự vẽ khung cửa sổ của
nó và khung đó nằm trong video — đã đo được màu khung chiếm 4,7–6,5% khung hình, và cờ `--app=` chỉ
giảm phần bị chiếm từ 144px xuống 57px chứ không xoá được. `Page.startScreencast` bắt surface của
TRANG, nên về cấu trúc không thể chứa UI trình duyệt — không phải "may ra sạch".

Lưu ý: `Page.captureScreenshot` (ảnh still) cũng chỉ chụp viewport, nên nó KHÔNG dùng để kiểm chứng
khung quay x11grab được — phải kiểm bằng đúng công nghệ sẽ xuất bản.

BA ĐIỀU PHẢI NHỚ (đều đã trả giá):
  1. CHỈ MỘT VÒNG ĐỌC websocket. Hai coroutine cùng gọi `ws.recv()` → ConcurrencyError. Vòng đọc
     duy nhất rẽ nhánh: có "id" → kết quả lệnh (set future); có "method" → sự kiện (đẩy hàng đợi).
  2. PHẢI ACK mỗi khung screencast (`Page.screencastFrameAck`), không thì Chrome ngừng gửi và ta
     sẽ tưởng "screencast chỉ ra vài khung".
  3. Screencast CHỈ gửi khung khi trang đổi. Đoạn tĩnh không sinh khung, nên khi encode phải
     HOLD khung cuối tới đúng thời lượng nhắm (`target_dur`), nếu không video cụt đúng đoạn hold.

Chạy thử:  python3 screencast_recorder.py --url file:///path/app/index.html --seconds 8 --out out.mp4
"""
import argparse
import asyncio
import base64
import errno
import json
import os
import subprocess
import time
import urllib.request

try:
    import websockets
except ImportError as e:      # pragma: no cover
    raise SystemExit("thiếu thư viện websockets: pip install websockets") from e


# ---------------------------------------------------------------- hiển thị X
def find_display(start=150, end=189):
    """Trả về display X trống đầu tiên, dọn lock mồ côi.

    KHÔNG tính display theo PID: tiến trình zombie của lượt chạy trước giữ display, làm Xvfb mới
    chết ngay với "Server is already active for display NN". Lock mồ côi (/tmp/.XNN-lock còn mà PID
    trong đó đã chết) cũng phải dọn, nếu không display đó bị loại oan mãi mãi sau một lần kill -9.
    """
    for n in range(start, end + 1):
        if os.path.exists("/tmp/.X11-unix/X%d" % n):
            continue                                   # X server thật đang nghe
        lock = "/tmp/.X%d-lock" % n
        if os.path.exists(lock):
            try:
                pid = int(open(lock, encoding="utf-8", errors="ignore").read().strip())
            except (OSError, ValueError):
                pid = None
            alive = False
            if pid:
                try:
                    os.kill(pid, 0)
                    alive = True
                except OSError as e:
                    alive = e.errno != errno.ESRCH
            if alive:
                continue                               # chủ lock còn sống
            try:
                os.remove(lock)                        # mồ côi → dọn
            except OSError:
                continue
        return ":%d" % n
    raise SystemExit("không tìm được display trống trong %d-%d" % (start, end))


def even_up(n):
    """Làm tròn LÊN số chẵn gần nhất.

    libx264 từ chối kích thước lẻ ("width not divisible by 2"). LỖI THẬT ĐÃ GẶP khi smoke test:
    viewport 1279px mà demo tính 1279 // 2 * 2 = 1278 (làm tròn XUỐNG) rồi pad=1278 — pad KHÔNG
    THỂ thu nhỏ khung nên ffmpeg chết với "return code -22 / Could not open encoder before EOF",
    một thông báo không chỉ ra nguyên nhân. Phải làm tròn LÊN.
    """
    return n + (n % 2)


def find_binary(*names):
    for n in names:
        p = os.environ.get(n.upper().replace("-", "_"))
        if p and os.path.exists(p):
            return p
        import shutil
        w = shutil.which(n)
        if w:
            return w
    return None


# ---------------------------------------------------------------- phiên CDP
class CDPSession:
    """Một phiên Chrome trong Xvfb, điều khiển qua CDP websocket.

    Vòng đời: `bat_dau()` (sync) → `await ket_noi()` → dùng → `dung()` trong finally.
    MỌI khởi động subprocess phải nằm trong try/finally: một lần SystemExit nổ giữa hàm khởi động
    khi nó còn NGOÀI try → finally không chạy → Chrome zombie giữ cổng và phá lượt chạy kế tiếp
    (triệu chứng gây nhầm: `bind() failed: Address already in use` rồi ws rơi xuống `ws://[::1]`,
    hoặc `/json` trả `[]` từ một Chrome zombie).
    """

    def __init__(self, url, width=1280, height=800, name="cdp"):
        self.url = url
        self.w = width
        self.h = height
        self.name = name
        self.disp = find_display()
        # cổng/profile theo PID để hai phiên không giành nhau
        self.port = 9300 + (os.getpid() % 600)
        self.profile = "/tmp/cdp_%s_%d" % (name, os.getpid())
        self.xvfb: "subprocess.Popen | None" = None
        self.chrome: "subprocess.Popen | None" = None
        self.ws: "websockets.ClientConnection | None" = None
        self._id = 0
        self._cho = {}          # id lệnh → Future
        self._su_kien = {}      # tên sự kiện → hàng đợi
        self._vong = None
        self.chrome_ui = 57     # px khung Chrome còn lại ở chế độ --app; đo lại bằng probe_geometry()

    # ---- tiến trình ----
    def bat_dau(self, chrome_ui=57):
        chrome = find_binary("google-chrome", "chromium", "chromium-browser")
        if not chrome:
            raise SystemExit("không tìm thấy google-chrome/chromium")
        subprocess.run(["rm", "-rf", self.profile])
        # màn hình X phải CAO HƠN viewport đúng bằng phần khung Chrome, để innerHeight đạt `height`.
        # Đã đo: --window-size 1280x800 + --app cho innerHeight 743 (Chrome chiếm 57px).
        xv = subprocess.Popen(
            ["Xvfb", self.disp, "-screen", "0",
             "%dx%dx24" % (self.w, self.h + chrome_ui)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.xvfb = xv
        time.sleep(2.0)
        if xv.poll() is not None:
            raise SystemExit("Xvfb %s chết ngay" % self.disp)
        self.chrome = subprocess.Popen(
            [chrome, "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
             "--no-first-run", "--no-default-browser-check", "--force-device-scale-factor=1",
             # KHÔNG --start-maximized: mâu thuẫn --window-size; quay màn hình cần kích thước
             # CHÍNH XÁC để khung hình khớp.
             "--app=" + self.url,
             "--window-size=%d,%d" % (self.w, self.h + chrome_ui), "--window-position=0,0",
             "--remote-debugging-port=%d" % self.port,
             "--remote-debugging-address=127.0.0.1",
             "--user-data-dir=" + self.profile],
            env=dict(os.environ, DISPLAY=self.disp),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    async def _doi_ws(self, timeout=30):
        """Lấy ws URL của page target. Thăm CẢ 127.0.0.1 lẫn [::1]: khi cổng IPv4 bị chiếm,
        Chrome in `DevTools listening on ws://[::1]:PORT` — chỉ thăm IPv4 sẽ chờ mòn rồi fail
        vào một Chrome khác đang trả lời /json."""
        cuoi = time.time() + timeout
        while time.time() < cuoi:
            chrome = self.chrome
            if chrome is not None and chrome.poll() is not None:
                break
            for h in ("127.0.0.1", "[::1]"):
                try:
                    with urllib.request.urlopen(
                            "http://%s:%d/json" % (h, self.port), timeout=3) as f:
                        ds = json.load(f) or []
                        for t in ds:
                            if t.get("type") == "page" and t.get("webSocketDebuggerUrl"):
                                return t["webSocketDebuggerUrl"]
                except Exception:
                    pass
            await asyncio.sleep(0.4)
        raise SystemExit("không lấy được ws URL (port %d, display %s) — Chrome sống=%s"
                         % (self.port, self.disp, self.chrome.poll() is None))

    async def ket_noi(self, override_dialogs=True):
        self.ws = await websockets.connect(await self._doi_ws(), max_size=None)
        self._vong = asyncio.create_task(self._doc_vong())
        await self.cmd("Runtime.enable")
        await self.cmd("Page.enable")
        if override_dialogs:
            # confirm()/alert() native trong Xvfb không ai bấm → treo trang đúng giữa lúc quay.
            await self.cmd("Page.addScriptToEvaluateOnNewDocument",
                           source="window.confirm=()=>true; window.alert=()=>{};")
        await self.cmd("Page.reload")
        await asyncio.sleep(2.0)

    async def _doc_vong(self):
        """VÒNG ĐỌC DUY NHẤT. Không nơi nào khác được gọi ws.recv()."""
        ws = self.ws
        if ws is None:
            return
        try:
            async for raw in ws:
                msg = json.loads(raw)
                mid = msg.get("id")
                if mid is not None and mid in self._cho:
                    self._cho.pop(mid).set_result(msg)
                    continue
                ten = msg.get("method")
                if ten:
                    q = self._su_kien.get(ten)
                    if q is not None:
                        q.put_nowait(msg.get("params", {}))
        except Exception:
            pass

    async def _send(self, obj):
        """MỘT chỗ duy nhất chạm ws. Báo lỗi rõ nếu gọi trước ket_noi(), thay vì
        AttributeError 'NoneType' object has no attribute 'send' khó đoán nguyên nhân."""
        ws = self.ws
        if ws is None:
            raise RuntimeError("chưa gọi ket_noi() — websocket chưa mở")
        await ws.send(json.dumps(obj))

    async def cmd(self, method, **params):
        self._id += 1
        mid = self._id
        fut = asyncio.get_event_loop().create_future()
        self._cho[mid] = fut
        await self._send({"id": mid, "method": method, "params": params})
        msg = await asyncio.wait_for(fut, timeout=40)
        if "error" in msg:
            raise RuntimeError("%s: %s" % (method, msg["error"]))
        return msg.get("result", {})

    async def gui(self, method, **params):
        """Gửi không chờ kết quả (dùng để ACK khung cho nhanh)."""
        self._id += 1
        await self._send({"id": self._id, "method": method, "params": params})

    def lang_su_kien(self, ten):
        q = asyncio.Queue()
        self._su_kien[ten] = q
        return q

    async def js(self, expr):
        r = await self.cmd("Runtime.evaluate", expression=expr, returnByValue=True)
        return r.get("result", {}).get("value")

    async def click(self, selector, index=0):
        """Bấm THẬT nhưng KHÔNG cuộn.

        Đừng gọi scrollIntoView trong helper click: nó cuộn trang tới vị trí TUỲ TIỆN của phần tử
        vừa bấm và phá framing (đã gặp: nội dung chính bị đẩy khuất, phần tử của bài khác lọt vào
        khung). Việc cuộn phải do một hàm khung quyết định bằng số đo, và phải xác nhận lại sau khi
        cuộn (kín vòng lặp) — kể cả khi toạ độ tài liệu đúng, header dính (sticky) có thể che mất
        phần trên viewport.
        """
        return await self.js(
            "(() => { const e=document.querySelectorAll('%s')[%d];"
            " if(!e) return 'KHONG_THAY';"
            " e.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));"
            " return 'OK'; })()" % (selector, index))

    async def probe_geometry(self):
        """Đo viewport thật — dùng để suy ra chrome_ui thay vì hardcode."""
        g = await self.js("JSON.stringify({w:innerWidth,h:innerHeight,sw:screen.width,sh:screen.height})")
        return json.loads(g)

    def dung(self):
        if self._vong:
            self._vong.cancel()
        for p in (self.chrome, self.xvfb):
            if not p:
                continue
            try:
                p.terminate(); p.wait(timeout=5)
            except Exception:
                try: p.kill()
                except Exception: pass
        subprocess.run(["rm", "-rf", self.profile])


# ---------------------------------------------------------------- quay + encode
async def record_shot(session, actions, duration, frame_dir, fps_target=30):
    """Quay một shot: chạy `actions(session)` trong lúc thu khung screencast.

    GHI KHUNG XUỐNG ĐĨA ngay khi nhận, chỉ giữ (timestamp, path) trong RAM: shot 95s ở 60fps × ~70KB
    ≈ 380MB nếu giữ bytes trong danh sách.

    `actions` là async callable nhận session — ở đó caller bấm nút/cuộn trang của app mình.
    Hàm này KHÔNG tự canh thời lượng bằng actions: nó chờ đủ `duration` giây kể từ lúc bắt đầu,
    nên actions phải tự chèn `await asyncio.sleep(...)` giữa các bước.
    """
    os.makedirs(frame_dir, exist_ok=True)
    q = session.lang_su_kien("Page.screencastFrame")
    await session.cmd("Page.startScreencast", format="jpeg", quality=90, everyNthFrame=1)
    meta = []
    t0 = time.time()
    stop = False

    async def thu():
        i = 0
        while not stop:
            try:
                p = await asyncio.wait_for(q.get(), timeout=0.4)
            except asyncio.TimeoutError:
                continue
            fp = os.path.join(frame_dir, "raw_%06d.jpg" % i)
            with open(fp, "wb") as f:
                f.write(base64.b64decode(p["data"]))
            # metadata.timestamp là đồng hồ Chrome; time.time() lúc nhận có độ trễ mạng
            meta.append((p.get("metadata", {}).get("timestamp") or time.time(), fp))
            await session.gui("Page.screencastFrameAck", sessionId=p["sessionId"])
            i += 1

    tac_vu = asyncio.create_task(thu())
    await actions(session)
    await asyncio.sleep(max(0.0, duration - (time.time() - t0)))
    await session.cmd("Page.stopScreencast")
    stop = True
    await asyncio.sleep(0.3)
    tac_vu.cancel()

    if meta:
        goc = meta[0][0]
        meta = [(t - goc, fp) for t, fp in meta]
    return meta


def encode(meta, out_mp4, target_dur, fps=30, width=1280, height=800, bg="0xFFFFFF"):
    """Resample khung screencast về lưới `fps` cố định THEO TIMESTAMP rồi mã hoá H.264.

    Ba điểm không được bỏ:
      · THỜI LƯỢNG = max(target_dur, timestamp khung cuối). Đoạn cuối tĩnh không sinh khung nào;
        lấy D = khung cuối thì video CỤT đúng đoạn hold. Khung cuối được giữ lặp tới hết target_dur.
      · PAD sang kích thước chẵn: libx264 từ chối kích thước lẻ ("width not divisible by 2"), mà
        viewport thật thường hụt 1px (1279 thay vì 1280). PAD bằng màu nền app chứ KHÔNG scale
        1279→1280, vì scale ngang sẽ kéo dãn chữ.
      · resample bằng SYMLINK, không copy, để không nhân đôi dung lượng đĩa.
    """
    if not meta:
        raise SystemExit("không có khung nào để encode")
    # tự làm chẵn và KHÔNG BAO GIỜ nhỏ hơn khung thật: scale giữ tỉ lệ cho vừa hộp rồi pad.
    # `pad` đơn thuần sẽ fail (-22) nếu đích nhỏ hơn khung — lỗi đã gặp thật ở smoke test.
    width = even_up(width)
    height = even_up(height)
    ffmpeg = find_binary("ffmpeg")
    if not ffmpeg:
        raise SystemExit("không tìm thấy ffmpeg")
    rs = os.path.join(os.path.dirname(meta[0][1]), "_rs")
    subprocess.run(["rm", "-rf", rs]); os.makedirs(rs)

    D = max(target_dur, meta[-1][0])
    if len(meta) <= 2:
        print("  [encode] chỉ %d khung: trang TĨNH nên screencast không gửi thêm — bình thường,"
              " khung cuối sẽ được giữ tới %.1fs" % (len(meta), D))
    n = int(round(D * fps))
    j = 0
    for i in range(n + 1):
        tgt = i / fps
        while j + 1 < len(meta) and meta[j + 1][0] <= tgt:
            j += 1
        link = os.path.join(rs, "f_%06d.jpg" % i)
        if os.path.lexists(link):
            os.remove(link)
        os.symlink(os.path.abspath(meta[j][1]), link)

    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
           "-framerate", str(fps), "-i", os.path.join(rs, "f_%06d.jpg"),
           # scale giảm (không tăng) cho vừa hộp, rồi pad phần thiếu bằng màu nền -> không bao giờ
           # kéo dãn và không bao giờ thu nhỏ. force_original_aspect_ratio=decrease giữ tỉ lệ.
           "-vf", "scale=%d:%d:force_original_aspect_ratio=decrease,"
                  "pad=%d:%d:(ow-iw)/2:(oh-ih)/2:color=%s,format=yuv420p"
                  % (width, height, width, height, bg),
           "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-movflags", "+faststart", out_mp4]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    subprocess.run(["rm", "-rf", rs])
    if r.returncode != 0:
        raise SystemExit("ffmpeg lỗi: " + (r.stderr or "")[-400:])
    return out_mp4


# ---------------------------------------------------------------- CLI tự kiểm
async def _demo(url, seconds, out):
    s = CDPSession(url, name="demo")
    tmp = "/tmp/cdp_demo_frames_%d" % os.getpid()
    try:
        s.bat_dau()
        await s.ket_noi()
        g = await s.probe_geometry()
        print("viewport %dx%d · display %s · port %d" % (g["w"], g["h"], s.disp, s.port))

        async def actions(sess):
            await asyncio.sleep(0.5)      # demo: chỉ để trang tự chạy

        meta = await record_shot(s, actions, seconds, tmp)
        print("thu %d khung · span %.1fs" % (len(meta), meta[-1][0] if meta else 0))
        encode(meta, out, seconds, width=even_up(g["w"]), height=even_up(g["h"]))
        print("-> %s (%d byte)" % (out, os.path.getsize(out)))
    finally:
        subprocess.run(["rm", "-rf", tmp])
        s.dung()


def main():
    ap = argparse.ArgumentParser(description="Quay web app bằng CDP screencast trên Xvfb")
    ap.add_argument("--url", required=True, help="URL app (file:// hoặc http://)")
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--out", default="out.mp4")
    a = ap.parse_args()
    asyncio.run(_demo(a.url, a.seconds, a.out))


if __name__ == "__main__":
    main()
