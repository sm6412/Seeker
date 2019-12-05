from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import ContactForm


# import models
from .models import QR_Code
from django.contrib.auth.models import User

@login_required
def home(request):
    user = request.user
    firstname = user.first_name
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
    fields = ['device']

    def form_valid(self,form):
        owner = self.request.user
        form.instance.owner = owner
        print(form.instance.id)
        return super().form_valid(form)

def emailView(request, device_id):
    code = QR_Code.objects.get(id=device_id)
    owner_email = code.owner.email
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [owner_email])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    context = {
        'form' : form,
        'device' : code.device,
    }
    return render(request, "home/email.html", context)

def successView(request):
    return HttpResponse('Success! Thank you for your message.')