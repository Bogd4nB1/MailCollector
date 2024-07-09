from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('mails/', views.mails, name='mails'),
    path('register_or_login/', views.register_or_login, name='register_or_login'),
    path('download_file/', views.download_file, name='download_file'),
]
