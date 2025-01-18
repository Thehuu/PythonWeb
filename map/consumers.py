# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    #Phương thức này được gọi khi một kết nối WebSocket mới được thiết lập.
    #Thêm kết nối WebSocket hiện tại vào nhóm notifications
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()

    #Phương thức này được gọi khi một kết nối WebSocket bị đóng.
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    #Phương thức này được gọi khi nhận được một thông điệp từ kết nối WebSocket.
    async def receive(self, text_data):
        pass

    #Phương thức này được gọi khi nhận được một thông báo từ nhóm notifications.
    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))