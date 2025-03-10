from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    date_posted = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'job_postings')

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete = models.CASCADE, related_name = 'applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'job_applications')
    applicant_name = models.CharField(max_length=200)
    applicant_email = models.EmailField()
    resume = models.FileField(upload_to = 'resumes/')
    cover_letter = models.TextField()
    date_applied = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.applicant_name} - {self.job.title}"