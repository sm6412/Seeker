from django.shortcuts import render
from django.http import HttpResponse

# import models
from .models import QR_Code

def home(request):
    context = {
        'qr_codes': QR_Code.objects.all(),
        'page_title' : 'Home'
    }
    return render(request,'home/home.html',context)
