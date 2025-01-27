# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
#from .models import ReliefLocation


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
    # Nó xử lý thông điệp nhận được, truy vấn cơ sở dữ liệu để lấy thông tin về điểm cứu trợ 
    # dựa trên incident_id, và gửi lại thông tin này qua WebSocket.
    async def receive(self, text_data):
        from .models import ReliefLocation
        data = json.loads(text_data)
        message = data['message']
        incident_id = data['incident_id']
        # Lấy đối tượng ReliefLocation từ cơ sở dữ liệu
        location = await sync_to_async(ReliefLocation.objects.get)(id=incident_id)
        await self.send(text_data=json.dumps({
            'message': message,
            # "incident_type": location.incident_type,
            'incident_id': location.id,
        }))


    #Phương thức này được gọi khi nhận được một thông báo từ nhóm notifications.
    # Nó xử lý thông báo, truy vấn cơ sở dữ liệu 
    # để lấy thông tin về điểm cứu trợ dựa trên incident_id
    async def send_notification(self, event):
        from .models import ReliefLocation
        message = event['message']
        incident_id = event['incident_id']

        # Lấy đối tượng ReliefLocation từ cơ sở dữ liệu
        location = await sync_to_async(ReliefLocation.objects.get)(id=incident_id)

        await self.send(text_data=json.dumps({
            'message': message,
            'incident_id': location.id
        }))