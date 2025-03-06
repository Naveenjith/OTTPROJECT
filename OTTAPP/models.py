from django.db import models
from django.contrib.auth.models import User


# Create your models here



class UserProfile(models.Model):
     user = models.OneToOneField('auth.user', on_delete=models.CASCADE)
     email= models.EmailField()
     phone_number= models.CharField(max_length=20)
     image = models.ImageField(upload_to='profileimage/',default='')

     def __str__(self):
         return  f"{self.user.username}"



class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video = models.FileField(upload_to='videos/')
    language = models.CharField(max_length=55,default='')

    def __str__(self):
        return self.title
    
    
class Subscription(models.Model):
    SUBSCRIPTION_PLANS = [
        ('basic', 'Basic Plan'),
        ('standard', 'Standard Plan'),
        ('premium', 'Premium Plan'),
        
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_plan = models.CharField(max_length=255,choices=SUBSCRIPTION_PLANS)  # You can customize this based on your subscription plans
 

    def __str__(self):
        return self.user.username


