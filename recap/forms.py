from django.forms import ModelForm
from django import forms
from .models import User

# Create a User form
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('lb_name', 'email')

        labels = {
        'lb_name': 'Letterboxd Username',
        'email': 'E-mail',
    }
        
class LoginForm(forms.Form):
    lb_name = forms.CharField(label='Letterboxd Username', max_length=30)
    email = forms.EmailField(label='E-mail', max_length=100)