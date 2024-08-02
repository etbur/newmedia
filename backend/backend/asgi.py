"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import  newpost.routing 
import marketplace.routing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = ProtocolTypeRouter({
  'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
           newpost.routing.websocket_urlpatterns+ marketplace.routing.websocket_urlpatterns
        ))
})
