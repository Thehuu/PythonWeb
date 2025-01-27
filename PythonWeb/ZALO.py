import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import websocket
import json
import threading

# Cấu hình WebDriver cho Chrome
chrome_options = Options()
chrome_options.binary_location = "/Users/huuthe/chrome/mac_arm-116.0.5793.0/chrome-mac-arm64/Chrome.app/Contents/MacOS/Google Chrome for Testing"
service = Service(executable_path="/Users/huuthe/chromedriver/mac_arm-116.0.5793.0/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Mở trang ZALO Web
driver.get("https://chat.zalo.me/")
time.sleep(25)  # Chờ người dùng đăng nhập

# Hàm xử lý khi nhận được thông báo từ WebSocket
#Chỗ này sẽ cần nhiều hơn là message chứ nhỉ
def on_message(ws, message):
    data = json.loads(message)
    notification_message = (
        f"Thông báo mới: {data.get('message', 'Không có tin nhắn')}\n"
        f"ID sự cố: {data.get('incident_id', 'N/A')}\n"
        f"Loại sự cố: {data.get('incident_type', 'N/A')}\n"
        f"Tên địa điểm: {data.get('location_name', 'N/A')}\n"
        f"Vĩ độ: {data.get('latitude', 'N/A')}\n"
        f"Kinh độ: {data.get('longitude', 'N/A')}\n"
        f"Mô tả: {data.get('description', 'N/A')}"
    )

    # Tìm ô nhập tin nhắn và gửi tin nhắn
    message_box = driver.find_element(By.CSS_SELECTOR, '#richInput')  # Ô nhập tin nhắn
    message_box.click()  # Click vào ô nhập tin nhắn để kích hoạt
    message_box.send_keys(notification_message)  # Nội dung tin nhắn từ WebSocket
    message_box.send_keys(Keys.RETURN)  # Nhấn Enter để gửi tin nhắn
    print(f"Đã gửi tin nhắn: {notification_message}")
    time.sleep(2)

# Kết nối WebSocket
def start_websocket():
    ws = websocket.WebSocketApp("ws://localhost:8000/ws/notifications/",
                                on_message=on_message)
    ws.run_forever()

# Chạy WebSocket trong một luồng riêng
websocket_thread = threading.Thread(target=start_websocket)
websocket_thread.daemon = True
websocket_thread.start()

# Giữ cho chương trình chạy liên tục
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    driver.quit()