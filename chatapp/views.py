from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages as django_messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message as ChatMessage
from .serializers import MessageSerializer
from django.contrib.auth import login, authenticate

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
@login_required
def poll_messages(request):
    messages = ChatMessage.objects.all().order_by('-id')[:20]
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

# 메시지 전송 API
@api_view(['POST'])
@login_required
def send_message(request):
    username = request.user.username  # 로그인한 사용자 이름
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Text is required'}, status=400)

    message = ChatMessage.objects.create(username=username, text=text)
    serializer = MessageSerializer(message)
    return Response(serializer.data)
