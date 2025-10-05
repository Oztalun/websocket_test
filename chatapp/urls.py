from django.urls import path
from . import views


urlpatterns = [
    path('poll/', views.poll_messages, name='poll_messages'),
    path('send/', views.send_message, name='send_message'),
]