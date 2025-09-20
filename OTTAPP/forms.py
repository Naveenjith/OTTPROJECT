from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Subscription, UserProfile, Movie, Genre, MovieRating
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        help_text='Required. Enter a valid email address.'
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number'
        }),
        help_text='Required. Enter a valid phone number.'
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        }),
        required=False
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Basic phone number validation
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Enter a valid phone number.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['subscription_plan']
        widgets = {
            'subscription_plan': forms.Select(attrs={
                'class': 'form-control',
                'id': 'subscription-plan'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subscription_plan'].empty_label = "Select a subscription plan"


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'phone_number', 'image', 'date_of_birth', 'bio']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself...'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise ValidationError("Enter a valid phone number.")
        if UserProfile.objects.filter(phone_number=phone_number).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone_number


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'release_date', 'thumbnail', 'video',
            'language', 'genre', 'duration', 'rating', 'certification',
            'director', 'cast', 'trailer_url', 'is_featured', 'is_trending'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'genre': forms.CheckboxSelectMultiple(),
            'duration': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '0.1'}),
            'certification': forms.Select(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'cast': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'trailer_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_trending': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 0 or rating > 10:
            raise ValidationError("Rating must be between 0 and 10.")
        return rating


class MovieRatingForm(forms.ModelForm):
    class Meta:
        model = MovieRating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10',
                'step': '0.1',
                'placeholder': 'Rate from 1 to 10'
            }),
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review...'
            })
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise ValidationError("Rating must be between 1 and 10.")
        return rating


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search movies...',
            'id': 'search-input'
        }),
        required=False
    )
    language = forms.ChoiceField(
        choices=[('', 'All Languages')] + Movie.LANGUAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        empty_label="All Genres",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )