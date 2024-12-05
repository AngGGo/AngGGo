from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")), # 메인페이지
    path('member/', include("member.urls")), # 로그인페이지
    path('event/', include("event.urls")), # 로그인페이지
]
