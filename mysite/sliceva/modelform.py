from django import forms
from django.forms import ModelForm
from sliceva.models import Device, User

class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ('host', 'loginmethod')

class UserForm(ModelForm):
    class Meta:
        model = User
        field = ('username', 'password', 'admin')
        widgets = {'password': forms.PasswordInput()}

