from django.urls import path
from .utils import WSMailConsumer


ws_urlpatterns = [
    path('ws/mail_get/', WSMailConsumer.as_asgi()),
]