from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import emailView, successView
from .views import DeviceCreateView, DeviceDetailView, DeviceDeleteView
from . import views

urlpatterns = [
    path('', views.home, name='seeker-home'),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('new/', DeviceCreateView.as_view(), name='device-create'),
    path('device/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),
    path('found_form/<int:device_id>/', emailView, name='found'),
    path('success/', successView, name='success'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='micro/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='micro/logout.html'), name='logout'),
]

