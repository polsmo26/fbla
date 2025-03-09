from django.contrib import admin
# from .models import JobPosting, JobApplication, Profile
from accounts.models import ApplicantProfile, EmployerProfile
from django.contrib.auth.models import User
from .models import JobPosting, JobApplication

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    # list_display = ('user', 'company_name')
    list_display = ('user',)
    
@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'date_posted', 'is_approved')
    list_filter = ('is_approved', 'date_posted')
    actions = ['approve_jobs']
    
    def approve_jobs(self, request, queryset):
        queryset.update(is_approved = True)
    approve_jobs.short_description = "Approve selected jobs"

# class JobPostingAdmin(admin.ModelAdmin):
#     list_display = ('title', 'company', 'date_posted', 'is_approved')
#     list_filter = ('is_approved',)
#     search_fields = ('title', 'company')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'date_applied')
    list_filter = ('job', 'date_applied')
    # search_fields = ('applicant_name', 'applicant_email', 'job__title')
    
# admin.site.register(JobPosting, JobPostingAdmin)
# admin.site.register(JobApplication, JobApplicationAdmin)
# admin.site.register(User)
# admin.site.register(Profile)