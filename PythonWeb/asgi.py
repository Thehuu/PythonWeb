"""
ASGI config for PythonWeb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import map.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PythonWeb.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Định tuyến các kết nối WebSocket đến các consumer 
            # dựa trên các URL pattern được định nghĩa trong routing.py.
            map.routing.websocket_urlpatterns
        )
    ),
})
