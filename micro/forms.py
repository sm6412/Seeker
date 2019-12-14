from django import forms

from utils.hints import set_user_for_sharding
from .models import Device
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)


class CreateDeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        exclude = ('user_id', )

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id')
        super(CreateDeviceForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        device = Device.objects.filter(user_id=self.user_id, name=name)
        set_user_for_sharding(device, self.user_id)

        if device.exists():
            raise forms.ValidationError("You already have a device with the same name!")
        return name
