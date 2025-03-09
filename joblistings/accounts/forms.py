from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    user_type = forms.ChoiceField(choices=[('applicant', 'Applicant'),('employer', 'Employer'),], widget=forms.RadioSelect)

    class Meta:
        model = CustomUser
        fields = ['name', 'username', 'email', 'password1', 'password2', 'user_type']