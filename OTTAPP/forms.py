from django import forms
from django.contrib.auth.forms import UserCreationForm
from.models import Subscription
from django.contrib.auth.models import User


class customUserCreatonForm(UserCreationForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'type':'data','class':'form-control'}))
    phone_number= forms.CharField(max_length=20)


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['subscription_plan']
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'phone_number', 'image']