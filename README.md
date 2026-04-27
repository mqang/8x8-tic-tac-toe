# 8x8 Tic-Tac-Toe

Đây là game cờ caro đơn giản chạy trong terminal. Bạn chơi quân `X`, máy chơi quân `O`. Ai nối được 4 ô liên tiếp trước thì thắng.

## Installation

Dự án cần Python 3.12 trở lên.

Nếu bạn dùng `uv`, chỉ cần chạy:

```bash
uv run python main.py
```

Nếu bạn chỉ có Python, hãy tạo môi trường ảo và cài thư viện:

```bash
python -m venv .venv
source .venv/bin/activate
pip install rich textual
python main.py
```

Trên Windows, dùng lệnh activate này thay cho dòng `source`:

```bash
.venv\Scripts\activate
```

## Gameplay

Bàn cờ có kích thước 8x8, gồm 64 ô. Người chơi đi trước với quân `X`, sau đó AI sẽ tự chọn nước đi cho quân `O`.

Mục tiêu rất đơn giản: nối 4 quân cùng loại liên tiếp theo hàng ngang, hàng dọc hoặc đường chéo.

## Hướng Dẫn Chơi

- Khi mở game, chọn cách điều khiển trước: nhấn `K` để dùng bàn phím hoặc `M` để dùng chuột.
- Nếu dùng bàn phím, dùng các phím mũi tên để chọn ô, rồi nhấn `Enter` hoặc `Space` để đánh.
- Nếu dùng chuột, click trực tiếp vào ô bạn muốn đánh.
- Nhấn `R` để chơi lại ván mới.
- Nhấn `Q` để thoát game.

## Test

```bash
uv run python -m unittest discover -s tests
```
