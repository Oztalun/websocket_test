from django.urls import path
from . import views


urlpatterns = [
    path('status/', views.poll_messages, name='poll_messages'),# 
    path('send/', views.send_message, name='send_message'),# POST만 받음, 데이터 보내는 기능/wpf, web 둘다 사용(name, text)/name은 request.host에서 가져옴
    # path('front/', views.view_message, name='view_message'),# GET만 받음, 그냥 위 두개에서 처리한 데이터를 보여주는 용도
]