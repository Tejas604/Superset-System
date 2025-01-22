from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    # Additional fields
    work_experience = forms.ChoiceField(
        choices=CustomUser.WORK_EXPERIENCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    educational_qualification = forms.ChoiceField(
        choices=CustomUser.EDUCATION_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    educational_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        help_text="Add specific details about your education (e.g., board, percentage, etc.)"
    )
    projects = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    certifications = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    previous_place_of_work = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    achievements = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    positions_of_responsibility = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',  # Username is required
            'email',     # Email is required (used as USERNAME_FIELD)
            'password1',  # Password field from UserCreationForm
            'password2',  # Confirmation password field from UserCreationForm
            'work_experience',
            'educational_qualification',
            'educational_description',
            'projects',
            'certifications',
            'previous_place_of_work',
            
            'achievements',
            'positions_of_responsibility',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
