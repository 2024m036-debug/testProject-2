from django.urls import path
from . import views

urlpatterns = [
    # トップページ：メール履歴一覧
    path('', views.email_list, name='email_list'),

    # 新規作成：メール作成画面
    path('create/', views.create_email, name='create_email'),

    # 詳細確認：メールの内容表示
    path('email/<int:pk>/', views.email_detail, name='email_detail'),

    # 編集：メールの内容修正
    path('email/<int:pk>/edit/', views.email_edit, name='email_edit'),

    # 削除：メールの削除
    path('email/<int:pk>/delete/', views.email_delete, name='email_delete'),
]