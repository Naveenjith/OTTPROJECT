from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta


# Create your models here

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='profileimage/', default='')
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"



class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Tamil', 'Tamil'),
        ('Telugu', 'Telugu'),
        ('Malayalam', 'Malayalam'),
        ('Kannada', 'Kannada'),
        ('Bengali', 'Bengali'),
        ('Marathi', 'Marathi'),
        ('Gujarati', 'Gujarati'),
        ('Punjabi', 'Punjabi'),
    ]

    RATING_CHOICES = [
        ('U', 'U'),
        ('U/A', 'U/A'),
        ('A', 'A'),
        ('S', 'S'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video = models.FileField(upload_to='videos/')
    language = models.CharField(max_length=55, choices=LANGUAGE_CHOICES, default='English')
    genre = models.ManyToManyField(Genre, related_name='movies')
    duration = models.DurationField(null=True, blank=True)
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    certification = models.CharField(max_length=10, choices=RATING_CHOICES, default='U')
    director = models.CharField(max_length=255, blank=True)
    cast = models.TextField(blank=True)
    trailer_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ['-created_at']
    
    
class Subscription(models.Model):
    SUBSCRIPTION_PLANS = [
        ('basic', 'Basic Plan'),
        ('standard', 'Standard Plan'),
        ('premium', 'Premium Plan'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.CharField(max_length=255, choices=SUBSCRIPTION_PLANS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    stripe_subscription_id = models.CharField(max_length=255, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan}"

    def is_subscription_active(self):
        return self.is_active and timezone.now() < self.end_date

    def save(self, *args, **kwargs):
        # Set end date based on plan
        if not self.end_date:
            if self.subscription_plan == 'basic':
                self.end_date = timezone.now() + timedelta(days=30)
            elif self.subscription_plan == 'standard':
                self.end_date = timezone.now() + timedelta(days=90)
            elif self.subscription_plan == 'premium':
                self.end_date = timezone.now() + timedelta(days=365)
        
        # Update is_active based on status and end_date
        self.is_active = self.status == 'active' and timezone.now() < self.end_date
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'movie']
        verbose_name = "Watchlist"
        verbose_name_plural = "Watchlists"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)]
    )
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'movie']
        verbose_name = "Movie Rating"
        verbose_name_plural = "Movie Ratings"

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - {self.rating}"


class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('movie_view', 'Movie View'),
        ('subscription', 'Subscription Change'),
        ('profile_update', 'Profile Update'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"


