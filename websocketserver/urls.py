from django.contrib import admin
from django.urls import path, include
from chatapp import views as chat_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 채팅 메시지 API
    path('', include('chatapp.urls')),
    path('admin/', admin.site.urls),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")