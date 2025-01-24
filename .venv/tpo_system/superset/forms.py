from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser,Company,AnswerSheet,Test,Resume,ScheduledTest
from django.contrib.auth import authenticate



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
    cgpa_or_percentage = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Enter your CGPA or percentage"
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
            'cgpa_or_percentage',
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

    def clean(self):
        cleaned_data = super().clean()
        educational_qualification = cleaned_data.get('educational_qualification')
        cgpa_or_percentage = cleaned_data.get('cgpa_or_percentage')

        if educational_qualification in ['Undergraduate', 'Postgraduate'] and not cgpa_or_percentage:
            self.add_error('cgpa_or_percentage', 'This field is required for Undergraduate and Postgraduate qualifications.')

        return cleaned_data
  

class CompanyRegistrationForm(UserCreationForm):
    class Meta:
        model = Company
        fields = [
            'name', 'email', 'password1', 'password2', 
            'qualification_criteria', 'job_description', 'salary', 
            'opportunity_type', 'duration', 'hiring_stages', 'role', 
            'date_of_visit', 'application_deadline', 'test_date', 
            'interview_date'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'qualification_criteria': forms.NumberInput(attrs={'class': 'form-control'}),
            'job_description': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opportunity_type': forms.Select(attrs={'class': 'form-select'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'hiring_stages': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_visit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'test_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'interview_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        company = super().save(commit=False)
        company.password = make_password(self.cleaned_data["password1"])  # Hash the password
        if commit:
            company.save()
        return company
    
# Custom login form
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))    

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email__iexact=email)
                if not user.check_password(password):
                    raise forms.ValidationError(
                        "Invalid password for the given email."
                    )
            except CustomUser.DoesNotExist:
                raise forms.ValidationError(
                    "No user found with this email address."
                )

        return self.cleaned_data

 

    
    
class CompanyDashboardForm(forms.ModelForm):
        class Meta:
            model = Company
            fields = ['test_date', 'qualification_criteria','hiring_stages','interview_date']
            widgets = {
                'test_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'interview_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                'hiring_stages': forms.Textarea(attrs={'rows': 3}),
            }

class TestCreationForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['test_date', 'description']
        widgets = {
            'test_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    def save(self, commit=True, company=None, qualified_students=None):
        test = super().save(commit=False)
        test.company = company
        test.qualified_students = qualified_students
        if commit:
            test.save()
            return test


        for student in qualified_students:
            ScheduledTest.objects.create(
                student=student,
                company=company,
                test_date=test.test_date,
                description=test.description
            )
        return test 

class AnswerSheetUploadForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ['file']

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']