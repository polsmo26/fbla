from django import forms
from .models import JobApplication, JobPosting

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'company', 'description', 'location', 'salary']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['applicant_name', 'applicant_email', 'resume', 'cover_letter']

class ContactForm(forms.Form): 
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)