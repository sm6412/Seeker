from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import ContactForm, CreateDeviceCodeForm
from django.core.mail import send_mail
from django.conf import settings

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
    template_name = 'home/qr_code_form.html'
    form_class = CreateDeviceCodeForm

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(CodeCreateView, self).get_initial(**kwargs)
        initial['device'] = ''
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CodeCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['owner'] = self.request.user
        return kwargs

def email_body(owner_device,finder_name,owner_name,finder_email):
    message = "Hi "+owner_name+",\n\n"
    message += "Looks like "+finder_name+" found one of your devices ("+owner_device+"). "
    message += "If you'd like to contact "+finder_name+" about retrieving it, their email is "+finder_email+".\n\n"
    message += "Best,\nSeeker"
    return message

def emailView(request, device_id):
    code = QR_Code.objects.get(id=device_id)
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            #owner_email = code.owner.email
            owner_email = settings.EMAIL_HOST_USER
            owner_device = code.device
            owner_name = code.owner.first_name
            subject = 'Found Device: '+owner_device
            from_email = settings.EMAIL_HOST_USER
            finder_name = form.cleaned_data['first_name']
            message = email_body(owner_device,finder_name,owner_name,form.cleaned_data['email'])
            try:
                send_mail(subject, message, from_email, [owner_email],fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')

    context = {
        'form' : form,
        'device' : code.device,
    }
    return render(request, "home/email.html", context)

def successView(request):
    return render(request, "home/success.html")