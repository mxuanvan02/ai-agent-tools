# AI Agent Tools

Curated, portable tools and skills for AI agents.

## Thư mục

### `thu-ky/` - Trợ lý cá nhân (Personal Secretary)

Workflow tái sử dụng cho trợ lý AI điều khiển máy tính:

- **Google Sheets**: quản lý tasks, events, habits, logs với Jev ra quyết định
- **Google Drive**: upload, phân loại, chuẩn hoá tên file, di chuyển giữa thư mục
- **Gmail/Calendar**: đồng bộ chỉ đọc, phân luồng mail bằng Jev
- **Browser automation**: jev-ultrafast cho tác vụ web

**Đặc điểm:**
- Jev (TypeSafe System-One) cho quyết định nhanh (~300ms, $0.00003/decision)
- Mọi thao tác ghi đều có verify sau ghi (read-back)
- Fail-closed cho config lỗi, fail-open cho Jev lỗi (fallback sang code)
- Dry-run mặc định cho mọi lệnh ghi

**Demo:**
```bash
# Thêm task
python3 thuky.py add "Soạn hồ sơ GVG" --deadline 2026-10-25 --priority 5 --effort 2

# Hỏi "hôm nay làm gì?"
python3 thuky.py today

# Upload và phân loại file Drive
python3 drive_ops.py classify-folder <folder_id>
```

## Cài đặt

```bash
# Clone
git clone https://github.com/mxuanvan02/ai-agent-tools.git
cd ai-agent-tools

# Dependencies
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# Cấu hình Google OAuth
# Xem ~/.hermes/skills/productivity/google-workspace/scripts/google_api.py

# Jev API key (optional, cho decision nhanh)
export TYPESAFE_API_KEY="your-key-here"
```

## Kiến trúc

```
thu-ky/
├── thuky.py          # CLI chính: tasks/events/habits/logs
├── gsh.py            # Google Sheets backend (verified read/write)
├── gsync.py          # Gmail/Calendar sync (read-only)
├── drive_ops.py      # Drive operations (upload, classify, rename)
└── _backups/         # Backup tự động trước khi xóa
```

## So sánh Jev vs LLM

| Tác vụ | Jev | LLM | Jev thắng |
|--------|-----|-----|-----------|
| Decision latency | ~300ms | ~8s | **25×** |
| Cost/decision | $0.00003 | $0.001+ | **30×** |
| Accuracy (pick task) | 100% | 100% | ngang |
| Reasoning capability | Thấp (chọn từ list) | Cao (mở) | LLM thắng |

**Kết luận:** Jev nhanh hơn cho tác vụ lặp, LLM tốt cho tác vụ cần suy luận.

## License

MIT
