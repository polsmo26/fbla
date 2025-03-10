#imports
from django.contrib import admin
from accounts.models import ApplicantProfile, EmployerProfile
from django.contrib.auth.models import User
from .models import JobPosting, JobApplication

#displays the applicants in the Applicants section of the profiles
@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

#displays the employers in the Employers section of the profiles
@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

#displays each job posted by the employers in the Job Postings section
@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'date_posted', 'is_approved')
    list_filter = ('is_approved', 'date_posted')
    actions = ['approve_jobs']
    #gives admin the power to approve job listings - jobs pending approval are not displayed in the site
    def approve_jobs(self, request, queryset):
        queryset.update(is_approved = True)
    approve_jobs.short_description = "Approve selected jobs"

#displays each application sent by an applicant in the Job Applications section
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'date_applied')
    list_filter = ('job', 'date_applied')