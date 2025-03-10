from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .models import JobPosting, JobApplication
from .forms import JobApplicationForm, ContactForm, JobPostingForm
from accounts.models import Profile


#basic pages
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def login(request):
    if request.method == 'POST':
        # connecting input fields to user profile
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        form = AuthenticationForm(request, data=request.POST)
        # if inputs are valid, user is logged in and a success message shows
        if form.is_valid():
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
    # if inputs are invalid, error message shows and user is prompted to retry the form
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#logout view
def custom_logout(request):
    logout(request)
    return redirect('/')

#job pages
def job_list(request):
    jobs = JobPosting.objects.filter(is_approved=True)
    return render(request, 'job_list.html', {'jobs':jobs})

def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    return render(request, 'job_detail.html', {'job':job})


# contact page
def contact(request):
    if request.method == "POST":
        # Extract form data from POST request
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        # Email subject & message body
        subject = f"New Contact Form Submission from {name}"
        message_body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}

        Message:
        {message}
        """

        # Send email with error handling
        try:
            send_mail(
                subject, 
                message_body, 
                settings.EMAIL_HOST_USER,  # From Email
                ['sandy.laine6@gmail.com'],  # To Email (spare email Polina has)
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send message: {e}")

        return redirect("contact") 
    return render(request, 'contact.html')


def contact_success(request):
    return render(request, "contact_success.html")

#login requirements
@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'employer':
        return redirect('index')
    job_postings = JobPosting.objects.filter(posted_by = request.user)
    applications = JobApplication.objects.filter(job__in=job_postings)
    return render(request, 'employer_dashboard.html', {'job_postings':job_postings, 'applications':applications})

@login_required
def applicant_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'applicant':
        return redirect('index')
    job_applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'applicant_dashboard.html', {'job_applications':job_applications})

@login_required
def apply_for_job(request, job_id):
    if request.user.profile.user_type != 'applicant':
        return redirect('index')
    job = get_object_or_404(JobPosting, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit = False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('applicant_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = JobApplicationForm()
    return render(request, 'apply_for_job.html', {'form':form, 'job':job})

@login_required
def post_job(request):
    if request.user.profile.user_type != 'employer':
        return redirect('index')
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted succesfully!')
            return redirect('employer_dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = JobPostingForm()
    return render(request, 'post_job.html', {'form':form})



# blog pages on the bottom of index page
def job_tips_page1(request):
    context = {
        "title": "🚀 Landing Your Dream Job: Top Tips for Success",
        "author_name": "Kelly Rowan",
        "post_date": "March 12, 2023",
        "read_time": "7",
        "content": "Learn the key strategies to make your job application stand out and impress recruiters.",
        "author_image": "https://i.imghippo.com/files/PA4969XUI.png",
        "article_image": "https://www.mediabistro.com/wp-content/uploads/2022/05/bigstock-Work-Passion-To-Motivate-And-I-424449374-1536x1024.jpg",
    }
    return render(request, "job_tips1.html", context)

def job_tips_page2(request):
    context = {
        "title": "💼 The Future of Work: Emerging Career Trends",
        "author_name": "Josiah Barclay",
        "post_date": "March 23, 2023",
        "read_time": "4",
        "content": "Discover the latest trends shaping the job market and how to prepare for them.",
        "author_image": "https://i.imghippo.com/files/wz7902tOw.jpg",
        "article_image": "https://www.classycareergirl.com/wp-content/uploads/2010/05/4-reasons-why-people-go-to-work.jpg",
    }
    return render(request, "job_tips2.html", context)

def job_tips_page3(request):
    context = {
        "title": "🎯 Resume Mistakes to Avoid & How to Fix Them",
        "author_name": "Evelyn Martinez",
        "post_date": "April 2, 2023",
        "read_time": "10",
        "content": "Make your resume recruiter-friendly with these simple yet powerful fixes.",
        "author_image": "https://i.imghippo.com/files/wT7919lY.png",
        "article_image": "https://theforage.wpengine.com/wp-content/uploads/2022/09/Depositphotos_95377176_L-1024x684.jpg",
    }
    return render(request, "job_tips3.html", context)