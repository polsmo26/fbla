from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm
from joblistings.forms import JobPostingForm
from .models import ApplicantProfile, EmployerProfile, Profile, CustomUser
from joblistings.models import JobPosting
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
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
            profile = Profile.objects.create(user=user, user_type=user_type)
            if user.user_type == 'applicant':
                ApplicantProfile.objects.create(user=user)
            elif user.user_type == 'employer':
                EmployerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully! You are now logged in.')
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

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