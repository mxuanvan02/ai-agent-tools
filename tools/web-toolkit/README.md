# web-toolkit

Ba module Python tái sử dụng, trích (và tổng quát hoá) từ các pattern tốt trong
`code-root/gmail-account-creator`. **Chỉ lấy phần kỹ thuật trung lập** — đã loại bỏ hoàn toàn
phần farm tài khoản / né captcha / giả fingerprint (xem ghi chú nguồn gốc bên dưới).

Cả 3 module thuần Python chuẩn, không dependency bên ngoài, không đụng mạng khi test.
29 test, 0 network, chạy trong ~0.1s:

```bash
cd ~/opt/web-toolkit
uv run --python 3.12 --with pytest python -m pytest test_web_toolkit.py -q
```

## 1. `proxy_pool.py` — pool proxy có lease, health-check, cooldown
Chọn proxy theo LRU/round-robin/random, tự nhả qua context manager (kể cả khi raise),
đếm lỗi liên tiếp với cooldown hàm mũ có trần, về hưu proxy chết sau `max_failures`,
health-probe injectable (không mạng mặc định). Không bao giờ lộ password qua `repr`/log.

```python
from proxy_pool import ProxyPool
pool = ProxyPool.from_file("proxies.txt")     # host:port[:user[:pass]]
with pool.acquire() as p:                      # tự release, exception -> tự tính là fail
    do_request(proxy=p.as_url(with_auth=False))
pool.check_health(probe=lambda p: ping(p))     # retire proxy chết
```

## 2. `humanize.py` — delay/gõ/chuyển động tự nhiên cho automation
Mục đích là **test bền**, không phải né phát hiện: sleep cố định là nguyên nhân số 1 gây
test flaky (action bắn trước khi listener gắn xong). Bảng delay theo loại action, jitter,
đường cong Bezier cho con trỏ, gõ từng ký tự có micro-pause. Transport-agnostic qua callback.

```python
from humanize import sleep_for, mouse_path, type_like_human
await sleep_for("before_click")                       # pause có jitter
pts = mouse_path(0, 0, 300, 200, steps=25)            # arc tự nhiên, endpoint chính xác
await type_like_human(page.type, text, mistake_chance=0.06)
```

## 3. `page_state.py` — máy trạng thái form khai báo
"Đang ở bước nào?" từ URL + phần tử hiện diện. Khai báo step bằng data, match URL trước
(rẻ, tin cậy) rồi tới element, trả về state có typed + suggested action. Cùng tư tưởng
checklist-driven với `~/opt/jev-exec-bench/jev_form_driver.py`. Chỉ cần 2 callback (url,
elements_present) nên test không cần mở browser.

```python
from page_state import PageStateMachine, PageState
machine = PageStateMachine([
    PageState("login", url_contains=["/login"], elements=["#password"], action="fill_credentials"),
    PageState("home",  url_contains=["/dashboard"], elements=["#user-menu"], action="done"),
])
state = machine.detect(url=page.url, elements_present=lambda s: page.locator(s).count() > 0)
```

## Nguồn gốc & phạm vi
Trích từ `code-root/gmail-account-creator` (ISC) — repo đó là công cụ tạo tài khoản Gmail
hàng loạt, vi phạm ToS Google; em **không** chạy hay khuyến nghị dùng nó. Ba module này là
phần kỹ thuật dùng được cho việc hợp pháp (proxy pool cho scraping có phép, timing cho test UI,
state machine cho wizard nhiều bước). Không chứa code captcha/SMS/anti-detect/fingerprint.
