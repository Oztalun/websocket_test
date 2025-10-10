from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages as django_messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message as ChatMessage
from .serializers import MessageSerializer
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.utils import timezone
import datetime

# 채팅 페이지
@login_required
def chat_home(request):
    return render(request, 'index.html')

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 가입 직후 자동 로그인
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('chat_home')  # 바로 채팅 페이지로 이동
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# 메시지 폴링 API
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def poll_messages(request):
    return Response({"status": "ok", "code": last_message}, status=200)

global last_message

# 메시지 전송 API -------------------------------------------------------
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def send_message(request):
    global last_message
    print("test")
    host = request.data.get('host')
    text = request.data.get('text')
    print(f"{host}    {text}")
    if not host:
        return Response({'error': 'Text is required'}, status=400)
    elif not text:
        return Response({'error': 'Host is required'}, status=400)
    elif len(host) > 50:
        return Response({'error': 'Text exceeds maximum length of 50'}, status=400)
    elif len(text) > 20:
        return Response({'error': 'Host exceeds maximum length of 20'}, status=400)
    elif "yy" in text:# 마지막 명령어 저장
        last_message = ChatMessage.objects.order_by('-timestamp').first().text
        return Response({"host":host, "text":text, "last_message":str(last_message)}, status=201)
    else:
        message = ChatMessage.objects.create(host=host, text=text)
        return Response({"host":host, "text":text}, status=201)
