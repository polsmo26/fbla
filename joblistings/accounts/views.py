#imports
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from joblistings.forms import JobPostingForm
from .models import ApplicantProfile, EmployerProfile, Profile, CustomUser
from joblistings.models import JobPosting
from django.contrib import messages

#register view
def register(request):
    if request.method == "POST":
        # importing UserRegistrationForm from accounts/forms.py
        form = UserRegistrationForm(request.POST)
        # form only takes inputs and saves if all of the inputs are valid
        if form.is_valid():
            user = form.save(commit=False)
            name = request.POST.get('name')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            user_type = request.POST.get('user_type')
            user_name = form.cleaned_data['name']
            user_type = form.cleaned_data.get('user_type')
            user.save()
            # new profile is created based on the user inputs
            profile = Profile.objects.create(user=user, user_type=user_type)
            # users created based on user type (applicant / employer)
            if user.user_type == 'applicant':
                ApplicantProfile.objects.create(user=user)
            elif user.user_type == 'employer':
                EmployerProfile.objects.create(user=user)
            # user is automatically logged in using their new user information
            login(request, user)
            # message is displayed to confirm success - extended from base.html
            messages.success(request, 'Account created successfully! You are now logged in.')
            return redirect('index')
    # if form is invalid, error message shows and user is prompted to retry filling out the form
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})