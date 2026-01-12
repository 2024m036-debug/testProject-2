from django.contrib import admin
from django.urls import path, include  # include を忘れずに！

urlpatterns = [
    # 管理画面
    path('admin/', admin.site.urls),

    # ▼▼▼ ログイン・ログアウト機能（これが必要です） ▼▼▼
    # これにより /accounts/login/ などが使えるようになります
    path('accounts/', include('django.contrib.auth.urls')),

    # アプリのURL（トップページなど）
    path('', include('testApp.urls')),
]