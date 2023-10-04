from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import Admin  # Import your Admin model
from .models import JobPosting
class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'email', 'mobile_number', 'date_of_birth']

class AdminPasswordResetForm(PasswordChangeForm):
    pass  # You can customize this form if needed
class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = ['title', 'description']
class JobSearchForm(forms.Form):
    location = forms.CharField(required=False)
    job_name = forms.CharField(required=False)
    type = forms.ChoiceField(choices=[('', 'Any'), ('full_time', 'Full Time'), ('part_time', 'Part Time')], required=False)        