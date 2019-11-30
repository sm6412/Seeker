from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required


# import models
from .models import QR_Code
from django.contrib.auth.models import User

@login_required
def home(request):
    user = request.user
    firstname = user.username
    codes = QR_Code.objects.filter(owner=user)
    num_of_codes = len(codes)
    context = {
        'name' : firstname,
        'code_num': num_of_codes,
        'qr_codes': codes,
        'page_title' : 'Home'
    }
    return render(request,'home/home.html',context)

class CodeDetailView(LoginRequiredMixin, DetailView):
    model = QR_Code

class CodeDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = QR_Code
    success_url = '/'
    
    def test_func(self):
        code = self.get_object()
        if self.request.user == code.owner:
            return True
        return False

class CodeCreateView(LoginRequiredMixin,CreateView):
    model = QR_Code
    fields = ['device','qr_code']

    def form_valid(self,form):
        owner = self.request.user
        form.instance.owner = owner
        return super().form_valid(form)
