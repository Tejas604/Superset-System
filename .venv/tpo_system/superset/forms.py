from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'work_experience', 'projects',
            'certifications', 'educational_qualification_12th', 'educational_qualification_degree',
            'previous_place_of_work', 'achievements', 'positions_of_responsibility'
        ]
