from django.urls import path
from . import views

urlpatterns = [
    path('site/login/<int:pk>/', views.login_page, name='login_page'),
    path('site/login/<int:pk>/json/', views.login_json, name='login_json'),

    path('<str:login>/', views.login_page_by_login, name='login_page_by_login'),
    path('<str:login>/json/', views.login_json_by_login, name='login_json_by_login'),

    path('login/<str:login>/', views.login_page_by_login, name='login_page_by_login_prefixed'),
    path('login/<str:login>/json/', views.login_json_by_login, name='login_json_by_login_prefixed'),
]
