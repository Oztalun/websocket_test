from django.urls import path
from . import views


urlpatterns = [
    path('status/', views.poll_messages, name='poll_messages'),
    path('send/', views.send_message, name='send_message'),
    path('front/', views.send_message, name='send_message'),
]