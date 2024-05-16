from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.get_users, name='get_all_users'),
    path('user/', views.user_manager),
    path('bank/', views.bank_manager)
]
