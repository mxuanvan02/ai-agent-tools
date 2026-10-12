# screencast-video-from-webapp

Agent Skill: quay **video demo từ một web app** trên máy Linux **không có màn hình thật** (server,
container, CI), bằng Chrome DevTools Protocol — không cần X server có window manager, không cần
công cụ ghi màn hình desktop, và **không dính UI trình duyệt vào video**.

> Nguyên tắc lõi: quay bằng `Page.startScreencast` (bắt surface của TRANG) thay vì
> `ffmpeg x11grab` (bắt cả màn hình X). Khác biệt không phải thẩm mỹ mà là cấu trúc:
> screencast **không thể** chứa thanh URL/tab/khung cửa sổ, còn x11grab thì gần như chắc chắn có.

## Điểm nổi bật

- **Một file, không framework**: `scripts/screencast_recorder.py` (~500 dòng, chỉ cần
  `websockets` + `ffmpeg` + `Xvfb` + Chrome). Đã smoke-test chạy độc lập.
- **Kiến trúc CDP một vòng đọc**: tránh `ConcurrencyError: cannot call recv while another
  coroutine is already running recv` — lỗi kinh điển khi viết client CDP bằng asyncio.
- **Resample theo timestamp + hold khung cuối**: screencast chỉ gửi khung khi trang ĐỔI, nên
  đoạn tĩnh không sinh khung nào. Encode phải hold khung cuối tới đúng thời lượng nhắm, nếu
  không video **cụt đúng đoạn giữ khung** — lỗi không hiện ở bất kỳ chỉ số kỹ thuật nào.
- **Chống zombie tiến trình**: tự tìm display trống, dọn lock mồ côi (`/tmp/.XNN-lock` mà PID đã
  chết), cổng/profile theo PID, mọi subprocess trong `try/finally`.
- **Kèm playbook "instrument sai"** (phần B của SKILL.md): bốn ca thật mà một công cụ đo in ra
  con số trông như đã kiểm chứng trong khi phép đo hỏng — lớp lỗi tốn giờ nhất khi dựng video
  có nghiệm thu tự động.

## Cài

```bash
# phụ thuộc hệ thống
sudo apt install xvfb            # hoặc: Xvfb có sẵn
# Chrome/Chromium bất kỳ; ffmpeg bất kỳ (cần libx264)
pip install websockets
```

## Dùng nhanh

```bash
# quay 8 giây một app local, xuất out.mp4
python3 scripts/screencast_recorder.py \
  --url file:///path/to/app/index.html --seconds 8 --out out.mp4
```

Nhúng vào pipeline riêng (bấm nút app của bạn trong lúc quay):

```python
import asyncio
from screencast_recorder import CDPSession, record_shot, encode, even_up

async def main():
    s = CDPSession("file:///path/app/index.html", width=1280, height=800)
    try:
        s.bat_dau()
        await s.ket_noi()

        async def actions(sess):
            await sess.click("#btn-start")          # bấm THẬT, không cuộn
            await asyncio.sleep(1.5)
            await sess.click(".item", 3)
            await asyncio.sleep(2.0)

        meta = await record_shot(s, actions, duration=12.0, frame_dir="/tmp/frames")
        g = await s.probe_geometry()
        encode(meta, "shot.mp4", target_dur=12.0,
               width=even_up(g["w"]), height=even_up(g["h"]))
    finally:
        s.dung()

asyncio.run(main())
```

## Những điều bắt buộc phải biết (đều đã trả giá)

| Vấn đề | Triệu chứng | Cách xử |
|---|---|---|
| Hai coroutine cùng `ws.recv()` | `ConcurrencyError` | chỉ `_doc_vong()` được đọc; `cmd()` await future |
| Không ACK khung | screencast "chỉ ra vài khung" | `Page.screencastFrameAck` mỗi khung, gửi one-way cho nhanh |
| `confirm()`/`alert()` trong Xvfb | trang treo giữa lúc quay | `Page.addScriptToEvaluateOnNewDocument` override **trước** khi reload |
| Zombie giữ display/cổng | `bind() failed: Address already in use`; `/json` trả `[]` | `find_display()` + khởi động trong `try/finally` |
| Chrome rơi xuống IPv6 | ws URL là `ws://[::1]` | thăm **cả** `127.0.0.1` và `[::1]` khi lấy ws URL |
| Kích thước lẻ | `width not divisible by 2`, ffmpeg `-22` | `even_up()` — làm tròn **LÊN**, không xuống |
| `pad` nhỏ hơn khung | ffmpeg `-22` "Could not open encoder before EOF" | dùng `scale=...:force_original_aspect_ratio=decrease,pad=...` |
| Lệch tỉ lệ (16:10 → 16:9) | chữ bị kéo dãn ngang | scale giữ tỉ lệ + pad bằng **màu nền app**, không stretch |
| Header dính (sticky) | nội dung bị che dù toạ độ đúng | đo chiều cao header, trừ khỏi vùng nhìn thấy, **xác nhận lại sau khi cuộn** |
| `scrollIntoView` trong helper click | framing hỏng ngẫu nhiên | bấm bằng `dispatchEvent`, cuộn do hàm khung quyết định |

## Verify video — ba lớp, thiếu một là chưa xong

1. **`ffprobe`**: độ phân giải / fps / codec / `pix_fmt=yuv420p` / duration. Cần nhưng KHÔNG đủ —
   video đen, đơ, sai framing vẫn đạt hết.
2. **Xem khung thật** tại ranh giới các shot: có UI trình duyệt không, chữ có bị cắt không, đúng
   cảnh không. Nếu vision tool lỗi thì đo hình học bằng pixel (crop-and-compare + biên thanh màu
   khác nền) — **hai phép độc lập**, đừng tin một phép.
3. **Đối chiếu số trên màn hình với nguồn dữ liệu**: số đọc được trong video phải truy về một file
   JSON/log thật. Spec/brief khai số khác số đo thì dùng số đo và khai rõ độ lệch.

## Giấy phép

MIT — xem `LICENSE`.
