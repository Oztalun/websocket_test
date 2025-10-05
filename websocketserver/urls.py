from django.contrib import admin
from django.urls import path, include
from chatapp import views as chat_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 회원가입
    path('accounts/signup/', chat_views.signup_view, name='signup'),

    # 로그인/로그아웃
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),

    # 채팅 페이지
    path('', chat_views.chat_home, name='chat_home'),

    # 채팅 메시지 API
    path('chat/', include('chatapp.urls')),
]
