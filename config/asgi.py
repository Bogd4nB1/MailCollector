from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter # type: ignore
from channels.auth import AuthMiddlewareStack # type: ignore
from channels.routing import URLRouter  # type: ignore
from appYandex.routing import ws_urlpatterns
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
    ),
})