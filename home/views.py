from django.shortcuts import render
from django.http import HttpResponse

# import models
from .models import QR_Code
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        user_name = request.user.username
        user = User.objects.filter(username=user_name).first()
        codes = QR_Code.objects.filter(owner=user)
        num_of_codes = len(codes)
        context = {
            'code_num': num_of_codes,
            'qr_codes': codes,
            'page_title' : 'Home'
        }
        return render(request,'home/logged_in_home.html',context)
    else:
        return render(request,'home/logged_out_home.html')


    
