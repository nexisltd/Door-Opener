"""
ASGI config for door project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from door import routing
from door.urls import urlpatterns 





os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'door.settings')

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(
            URLRouter(
                urlpatterns
            )

        )
    }
)
