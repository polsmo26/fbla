#imports
from django import forms
from .models import JobApplication, JobPosting

#assigns fields for job posting form - for employers
class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'company', 'description', 'location', 'salary']

#assigns fields for job application form - for applicants
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['applicant_name', 'applicant_email', 'resume', 'cover_letter']

#assigns fields for contact form - for any user with an inquiry
class ContactForm(forms.Form): 
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)