from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
# from django.contrib import messages
from django.conf import settings
from .models import JobPosting, JobApplication
from .forms import JobApplicationForm, ContactForm, JobPostingForm
from accounts.models import Profile


#basic pages
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Error: Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    # return render(request, 'login.html')

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
            messages.error(request, 'Error found in form')
    else:
        form = JobPostingForm()
    return render(request, 'post_job.html', {'form':form})



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # # (Optional) Send an email notification
        # send_mail(
        #     subject=f"New Contact Form Submission from {name}",
        #     message=f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}",
        #     from_email='your-email@example.com',  # Replace with your email
        #     recipient_list=['your-email@example.com'],  # Replace with your email
        #     fail_silently=False,
        # )

        # Flash a success message
        messages.success(request, "Your message has been successfully sent!")

        return redirect('contact_success')  # Redirect to a success page

    return render(request, "contact.html")

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
    # print("job applications:", job_applications)
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
            # application.applicant_name = request.user.username
            # application.applicant_email = request.user.email
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('applicant_dashboard')
        else:
            messages.error(request, 'Error found in form')
        
    else:
        form = JobApplicationForm()
    return render(request, 'apply_for_job.html', {'form':form, 'job':job})

def contact_view(request):
    if request.method == "POST":
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

        # Send email
        send_mail(
            subject, 
            message_body, 
            settings.EMAIL_HOST_USER,  # From Email
            ['your-email@example.com'],  # To Email (replace with your email)
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")  # Redirect back to contact page

    return render(request, "contact.html")



# def register(request):
#     if request.method == "POST":
#         # form = UserCreationForm(request.POST)
#         name = request.POST.get('name')
#         username = request.POST.get('username')
#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')
#         user_type = request.POST.get('user_type')
#         if password1 != password2:
#             messages.error(request, "Passwords do not match.")
#             return redirect('register')

#         if CustomUser.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect('register')
        
#         user = CustomUser.objects.create_user(
#             username=username,
#             password=password1,
#             name=name,
#             user_type=user_type,
#         )
#         messages.success(request, "Account created successfully!")
#         return redirect('login')
#         # if form.is_valid():
#         #     form.save()
#         #     messages.success(request, "Account created successfully!")
#         #     return redirect('login')
#         # else:
#             # messages.error(request, 'Error in form submission!')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', {'form':form})
