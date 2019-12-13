from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, DeleteView
from .forms import ContactForm, CreateDeviceForm, UserRegisterForm
from utils.hints import set_user_for_sharding

from .models import Profile, Device

@login_required
def home(request):
    user = request.user
    first_name = user.first_name
    devices = Device.objects.filter(user_id=user.id)
    set_user_for_sharding(devices, user.id)
    num_devices = len(devices)
    context = {
        'name': first_name,
        'devices': devices,
        'num_devices': num_devices,
        'page_title' : 'Home',
    }
    return render(request, 'micro/home.html', context)


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device


class DeviceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Device
    success_url = '/'

    def test_func(self):
        device = self.get_object()
        if self.request.user.id == device.user_id:
            return True
        return False


class DeviceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'micro/device_form.html'
    form_class = CreateDeviceForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(DeviceCreateView, self).get_initial(**kwargs)
        initial['name'] = ''
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DeviceCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user_id'] = self.request.user.id
        return kwargs


def email_body(device_name, finder_name, owner_name, finder_email):
    message = "Hi, %s:\n\n" % owner_name
    message += "Looks like %s has found one of your devices (%s). " % (finder_name, device_name)
    message += "If you'd like to contact %s about retrieving the device, " % finder_name
    message += "their email is %s.\n\nBest,\nSeeker" % finder_email
    return message


def emailView(request, device_id):
    device = Device.objects.get(id=device_id)
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            owner = Profile.objects.get(user_id=device.user_id)

            owner_email = owner.email
            owner_name = owner.first_name
            device_name = device.name

            subject = 'Found Device: %s' % device_name
            from_email = settings.EMAIL_HOST_USER
            finder_name = form.cleaned_data['first_name']
            body = email_body(device_name, finder_name, owner_name, form.cleaned_data['email'])

            try:
                send_mail(subject, body, from_email, [owner_email], fail_silently=False)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')

    context = {
        'form': form,
        'device': device.name,
    }
    return render(request, "micro/email.html", context)


def successView(request):
    return render(request, "micro/success.html")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=True)
            u = Profile(
                user_id=new_user.id, username=new_user.username,
                first_name=new_user.first_name, last_name=new_user.last_name,
                email=new_user.email
            )
            u.save()
            messages.success(request, f'Your account has been created! You can now log in!')
            return redirect('login')

    form = UserRegisterForm()
    return render(request, 'micro/register.html', {'form': form})


def profile(request):
    return render(request, 'micro.profile.html')

