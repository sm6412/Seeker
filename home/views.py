from django.shortcuts import render
from django.http import HttpResponse

codes = [
    {
        'device_name' : "Samira's iPhone",
        'qr_code' : "1234"
    },
    {
        'device_name' : "Samira's calculator",
        'qr_code' : "1235"
    }
]

def home(request):
    context = {
        'qr_codes':codes,
        'page_title' : 'Home'
    }
    return render(request,'home/home.html',context)
