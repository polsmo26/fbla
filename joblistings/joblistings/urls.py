#imports
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from . import views
from .views import * 

urlpatterns = [
    #basic urls
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('faq/', views.faq, name='faq'),
    path('register/', accounts_views.register, name='register'),
    path('login/', views.login, name='login'),
    path("job-tips1/", job_tips_page1, name="job_tips1"),
    path("job-tips2/", job_tips_page2, name="job_tips2"),
    path("job-tips3/", job_tips_page3, name="job_tips3"),
    #accounts urls
    path("accounts/", include('accounts.urls')),
    #job urls
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('post-job/', views.post_job, name='post_job'),
    #login requirement urls
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('applicant-dashboard/', views.applicant_dashboard, name='applicant_dashboard'), 
    path('logout/', views.custom_logout, name='logout'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
