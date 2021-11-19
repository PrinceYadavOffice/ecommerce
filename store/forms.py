from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields
from .models import Customer, Product

class SetquantityForm(forms.Form):    
    quantity = forms.CharField(widget=forms.NumberInput(
        attrs={
            'min':1,            
            'value':1,
            'max':5
        }
    ))

    
   

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )     


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    phone = forms.CharField(max_length=10)
    address = forms.CharField(max_length=250)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        Customer.objects.create(user=user,phone = self.cleaned_data['phone'], address = self.cleaned_data['address'])        
        return user    

    