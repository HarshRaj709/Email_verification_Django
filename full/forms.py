from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User

class Extradata(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

class EditUserData(UserChangeForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','date_joined','last_login','is_active','is_staff']
        