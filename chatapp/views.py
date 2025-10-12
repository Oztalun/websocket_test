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
import os
from dotenv import load_dotenv
load_dotenv()
server_url = os.getenv("SERVER_URL")

# # 채팅 페이지
# @login_required
# def chat_home(request):
#     return render(request, 'index.html')

# # 회원가입
# def signup_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # 가입 직후 자동 로그인
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('chat_home')  # 바로 채팅 페이지로 이동
#     else:
#         form = UserCreationForm()
#     return render(request, 'signup.html', {'form': form})

global last_message


# 메시지 폴링 API
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def poll_messages(request):
    message = check_message()
    if message is None:
        print("No messages found")
        return Response({'error': 'No messages found'}, status=200)
    elif message is False:
        message = ChatMessage.objects.order_by('-timestamp').first()
        print(f"\n\nhost: {message.host}\ntext: {message.text}\nis_working: {message.is_working}\namswer_time: {message.timestamp}\n대답 받음\n")
        return Response({"host":message.host, "text":message.text, "is_working":message.is_working, "answer_time": message.timestamp}, status=200)
    elif message.timestamp < timezone.now() - datetime.timedelta(seconds=10):
        message.is_working = False
        message.save()
        print("failed to get result code in time, set is_working to False")
        return Response({"host":message.host, "text":message.text, "is_working":message.is_working, "answer_time": message.timestamp, 'ps':'timeout, false due to failure'}, status=200)
    print('대답 대기중\n')
    return Response({"status": "ok", "value": message.is_working, "code": message.text}, status=200)


# 메시지 전송 API -------------------------------------------------------
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def send_message(request):
    global last_message
    host = request.data.get('host')
    text = request.data.get('text')
    print(f"\n{host}    {text}\n")
    determine = check_message()
    if not host:
        print("host is required")
        return Response({'error': 'failed', 'code': 'Text is required'}, status=401)
    elif not text:
        print("text is required")
        return Response({'error': 'failed', 'code': 'Host is required'}, status=402)
    elif len(host) > 50:
        print("host is too long")
        return Response({'error': 'failed', 'code': 'Text exceeds maximum length of 50'}, status=400)
    elif len(text) > 20:
        print("text is too long")
        return Response({'error': 'failed', 'code': 'Host exceeds maximum length of 20'}, status=400)
    # 기록이 없으면
    elif determine is False or determine is None:# 기록이 없거나 대답을 받았으면
        message = ChatMessage.objects.create(host=host, text=text)
        print(f"host: {message.host}, text: {message.text}, is_working: {message.is_working}, timestamp: {message.timestamp}")
        return Response({"host":host, "text":text}, status=201)
    # 마지막 메시지의 is_working이 None이면(결과 코드가 안왔으면)
    elif "yy" in text:#결과 코드 받았으면
        last_message.is_working = True
        last_message.save()
        print(f"host: {last_message.host}, text: {last_message.text}, is_working: {last_message.is_working}")
        return Response({"is_working":last_message.is_working}, status=201)
    elif "nn" in text:#결과 코드 받았으면
        last_message.is_working = False
        last_message.save()
        print(f"host: {last_message.host}, text: {last_message.text}, is_working: {last_message.is_working}")
        return Response({"is_working":last_message.is_working}, status=201)
    elif (timezone.now() - last_message.timestamp) < datetime.timedelta(seconds=10):#10초 이내에 다시 요청이 오면
        return Response({'error': 'Please wait before sending another message'}, status=200)#400 하니까 html에 안나옴 ㅋㅋㅋ
    else:
        last_message.is_working = False
        last_message.save()
        print("failed to get result code in time, set is_working to False")
        return Response({'error': 'Failed', "code":"failed to get result code in time, set is_working to False"}, status=205)

# mobile 프론트 -------------------------------------------------------
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def view_message(request):
    return render(request, 'front.html', {"server_url": server_url})

def check_message():
    global last_message
    if not ChatMessage.objects.exists():# 기록이 있을 때(없을 때 하면 에러나서)
        return None
    if ChatMessage.objects.order_by('-timestamp').first().is_working is None: # 마지막 메시지의 is_working이 None이면(결과 코드가 안왔으면)
        last_message = ChatMessage.objects.order_by('-timestamp').first()
        return last_message
    else:# 마지막 메시지의 is_working이 None이 아니면(결과 코드가 왔으면)
        return False