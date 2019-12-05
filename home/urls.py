from django.urls import path
from django.contrib import admin
from .views import emailView, successView
from .views import CodeCreateView, CodeDetailView, CodeDeleteView
from . import views

urlpatterns = [
    path('', views.home,name='seeker-home'),
    path('qr_code/<int:pk>/',CodeDetailView.as_view(), name = 'code-detail'),
    path('new/',CodeCreateView.as_view(),name ='code-create'),
    path('qr_code/<int:pk>/delete/',CodeDeleteView.as_view(), name = 'code-delete'),
    path('found_form/<int:device_id>/', emailView, name='found'),
    path('success/', successView, name='success'),
    

]