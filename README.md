# Weather Sentinel

Weather Sentinel lấy dự báo 7 ngày từ Open-Meteo bằng model ECMWF, in kết quả
ra terminal và gửi bản tin qua Telegram. Bản tin gồm xác suất mưa cao nhất và
tổng lượng mưa theo ngày, cùng danh sách giờ đạt các ngưỡng lọc đã cấu hình.

## Yêu cầu

- Python 3.11 trở lên
- Kết nối Internet để gọi Open-Meteo và Telegram Bot API
- Telegram bot và `chat_id` nhận tin nhắn

## Cấu hình

### 1. Thiết lập Telegram

Tạo file `.env` ở thư mục gốc dự án:

```dotenv
TELEGRAM_TOKEN=token_bot_cua_ban
TELEGRAM_CHAT_ID=id_chat_cua_ban
LATITUDE=<nhap_vi_do>
LONGITUDE=<nhap_kinh_do>
```

Không chia sẻ hoặc commit file `.env`. File này chứa thông tin bí mật của bot.
Thay `<nhap_vi_do>` và `<nhap_kinh_do>` bằng tọa độ địa điểm của bạn; chương
trình đọc hai giá trị này từ file `.env`.

### 2. Thiết lập địa điểm và dự báo

Chỉnh các giá trị trong [`config.yaml`](./config.yaml):

```yaml
timezone: Asia/Ho_Chi_Minh
days: 7
min_rain_mm: 0.5
rain_probability_threshold: 50
model: ecmwf_ifs
```

- `LATITUDE`, `LONGITUDE` trong `.env`: tọa độ địa điểm cần dự báo.
- `timezone`: múi giờ dùng cho giờ/ngày trong dự báo.
- `days`: số ngày dự báo (hiện đặt là 7).
- `min_rain_mm`: lượng mưa tối thiểu theo giờ để liệt kê trong phần dự báo
  theo giờ.
- `rain_probability_threshold`: xác suất mưa tối thiểu theo giờ để liệt kê
  khung giờ dễ mưa (mặc định 50%).
- `model`: model dự báo duy nhất đang sử dụng.

## Chạy thử trên máy tính

Mở terminal tại thư mục dự án.

### macOS / Linux

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

### Windows PowerShell

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

Lần chạy này gọi API dự báo, in bảng 7 ngày ra terminal và gửi một tin nhắn
thật tới Telegram. Để kiểm tra lại sau này, kích hoạt môi trường ảo rồi chạy
`python main.py`. Dự án hiện chưa có bộ unit test tự động.

Nếu chỉ cần kiểm tra lỗi cú pháp Python mà không gọi API hoặc gửi tin nhắn:

```bash
python -m compileall -q main.py config display notifier services weather
```

## Cài đặt và chạy định kỳ trên Ubuntu VPS

Các lệnh sau giả sử VPS dùng tài khoản `ubuntu` và dự án được đặt tại
`/home/ubuntu/weather-sentinel`. Thay đường dẫn này nếu bạn cài dự án ở nơi
khác.

### 1. Cài Python và công cụ cần thiết

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
python3 --version
```

Đảm bảo phiên bản Python là 3.11 trở lên.

### 2. Tải dự án lên VPS

Nếu dự án nằm trên GitHub, clone repository:

```bash
git clone <URL-repository-cua-ban> /home/ubuntu/weather-sentinel
cd /home/ubuntu/weather-sentinel
```

Hoặc sao chép thư mục dự án lên VPS, rồi chuyển đến thư mục đó:

```bash
cd /home/ubuntu/weather-sentinel
```

### 3. Cài môi trường ảo và dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Cấu hình và chạy thử

Tạo file `.env` trong thư mục gốc dự án:

```bash
nano .env
```

Thêm thông tin bot, lưu file rồi giới hạn quyền đọc:

```dotenv
TELEGRAM_TOKEN=token_bot_cua_ban
TELEGRAM_CHAT_ID=id_chat_cua_ban
LATITUDE=<nhap_vi_do>
LONGITUDE=<nhap_kinh_do>
```

```bash
chmod 600 .env
```

Thay các giá trị mẫu của `LATITUDE` và `LONGITUDE` bằng tọa độ cần dự báo, sau
đó chạy thử:

```bash
cd /home/ubuntu/weather-sentinel
.venv/bin/python main.py
```

Lệnh trên phải in dự báo và gửi tin nhắn Telegram. Nếu có lỗi, kiểm tra lại
token, `chat_id`, kết nối mạng và cấu hình trước khi tạo lịch tự động.

### 5. Lên lịch chạy mỗi ngày bằng cron

Nếu terminal báo `crontab: command not found`, cài và bật dịch vụ cron:

```bash
sudo apt update
sudo apt install -y cron
sudo systemctl enable --now cron
```

Kiểm tra lệnh đã khả dụng:

```bash
command -v crontab
systemctl status cron --no-pager
```

Mở crontab của tài khoản đang chạy dự án:

```bash
crontab -e
```

Thêm dòng sau để chạy mỗi ngày lúc 07:00 theo múi giờ của VPS, đồng thời ghi
đầu ra vào file log:

```cron
0 7 * * * cd /home/ubuntu/weather-sentinel && .venv/bin/python main.py >> weather-sentinel.log 2>&1
```

Nếu muốn 07:00 theo giờ Việt Nam, đặt múi giờ VPS trước:

```bash
sudo timedatectl set-timezone Asia/Ho_Chi_Minh
timedatectl
```

Lưu crontab rồi kiểm tra lịch đã được lưu:

```bash
crontab -l
```

Xem log sau lần chạy:

```bash
tail -n 100 /home/ubuntu/weather-sentinel/weather-sentinel.log
```

Cron sử dụng đúng môi trường ảo và thư mục dự án trong lệnh trên. Không đưa
token Telegram vào crontab; chương trình đọc token từ file `.env`.
