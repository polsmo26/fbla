#imports
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.conf import settings

#Defining a Profile model to extend the default User model
class Profile(models.Model):
    #creating a one-to-one relationship with the default User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #defining the user choices for any given profile
    USER_TYPES = [
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    #string representation of the Profile model
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

#Defining a model specifically for Applicant profiles
class ApplicantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applicant_profile")
    def __str__(self):
        return f"{self.user.username} (Applicant)"
    
#Defining a model specifically for Employer profiles
class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employer_profile")
    def __str__(self):
        return f"{self.user.username} (Employer)"

#Defining a CustomUser model that extends Django's built-in AbstractUser
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    )
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Fix conflicts by adding unique related_name attributes
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username

