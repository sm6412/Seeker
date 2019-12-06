from django import forms

# import models
from .models import QR_Code
from django.contrib.auth.models import User

# contact form
class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(required=True)

class CreateDeviceCode(forms.ModelForm):
    class Meta:
        model = QR_Code
        exclude = ('owner',)

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super(CreateDeviceCode, self).__init__(*args, **kwargs)

    def clean_device(self):
        device = self.cleaned_data['device']
        if QR_Code.objects.filter(owner=self.owner, device=device).exists():
            raise forms.ValidationError("You have already have a device with the same name!")
        return device