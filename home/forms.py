from django import forms

# contact form
class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(required=True)