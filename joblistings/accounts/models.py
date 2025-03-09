# from django.db import models
# from django.contrib.auth.models import AbstractUser
# # Create your models here.
# class CustomUser(AbstractUser):
#     USER_TYPE_CHOICES = (
#         ('applicant', 'Applicant'),
#         ('employer', 'Employer'),
#     )
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='applicant')

#     def __str__(self):
#         return self.username

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    USER_TYPES = [
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class ApplicantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applicant_profile")
    # resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Example field
    # applied_jobs = models.ManyToManyField('joblistings.Job', blank=True)  # Example relationship

    def __str__(self):
        return f"{self.user.username} (Applicant)"

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employer_profile")
    # company_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} (Employer)"


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    )
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # Fix conflicts by adding unique related_name attributes
    # groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def __str__(self):
        return self.username
