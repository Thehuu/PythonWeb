# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):

    #Phương thức này được gọi khi một kết nối WebSocket mới được thiết lập.
    #Thêm kết nối WebSocket hiện tại vào nhóm notifications
    async def connect(self):
        await self.channel_layer.group_add("notifications", self.channel_name)
        await self.accept()
    
    

    #Phương thức này được gọi khi một kết nối WebSocket bị đóng.
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)

    #Phương thức này được gọi khi nhận được một thông báo từ nhóm notifications (trong file views.py)
    # Nó xử lý thông báo, truy vấn cơ sở dữ liệu 
    async def send_notification(self, event):
        from .models import ReliefLocation
        message = event['message']
        incident_id = event['incident_id']
        # Lấy đối tượng ReliefLocation từ cơ sở dữ liệ
        location = await sync_to_async(ReliefLocation.objects.get)(id=incident_id)

        await self.send(text_data=json.dumps({
            'message': message,
            'name': location.name, 
            'mobile': location.mobile,
            'incident_id': location.id,
            'incident_type': location.incident_type,
            'latitude': location.latitude,
            'longitude': location.longitude,
            'description': location.description,
            'created_at': location.created_at.strftime('%d/%m/%Y %H:%M')
        }))