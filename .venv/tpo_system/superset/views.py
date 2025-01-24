from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.utils.timezone import now
from .forms import CustomUserRegistrationForm, CompanyRegistrationForm , CustomLoginForm
from .forms import CompanyDashboardForm,AnswerSheetUploadForm,TestCreationForm
from .models import CustomUser, Company ,Resume,ScheduledTest
from django.contrib.auth.models import User
from .backend import EmailBackend 



def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()  # Save the user to the database
            user.backend = 'superset.backend.EmailBackend'  # Explicitly set the backend
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('home')
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Registration failed. Please check the form and try again.")
    else:
        form = CustomUserRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)



def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                company = form.save()  # Use the save method which handles password hashing
                company.backend = 'superset.backend.EmailBackend'  # Explicitly set the backend
                login(request, company)  # Log in the new company user
                messages.success(request, "Company registration successful!")
                return redirect('company_dashboard')
            except IntegrityError as e:
                messages.error(request, f"Error: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            messages.error(request, "Company registration failed. Please check the form and try again.")
    else:
        form = CompanyRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'company_register.html', context)





def home(request):
    return render(request, 'home.html')



def custom_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' field corresponds to the email
            password = form.cleaned_data.get('password')
            # Specify the backend when authenticating
            user = authenticate(request, email=email, password=password, backend='superset.backend.EmailBackend')
            print(user)  # Check what this prints in your console
            
            if user is not None:
                login(request, user)
                # Redirect based on the user type
                if hasattr(user, 'company'):  # Check if user is a Company
                    return redirect('company_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            # Debug statement to print form errors
            print(form.errors)
            messages.error(request, "Invalid form submission.")
    else:
        form = CustomLoginForm()

    context = {
        'form': form
    }
    return render(request, 'login.html', context)

# Forms for editing and uploading
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'work_experience', 'projects', 'certifications',
            'educational_qualification', 'educational_description',
            'previous_place_of_work', 'achievements', 'positions_of_responsibility'
        ]


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']


@login_required
def student_dashboard(request):
    """View to manage the student dashboard."""
    user = request.user
    resumes = Resume.objects.filter(user=user)
    companies = Company.objects.filter(date_of_visit__gte=now().date()).order_by('date_of_visit')
    scheduled_tests = ScheduledTest.objects.filter(student=user)

    if request.method == "POST":
        if 'edit_profile' in request.POST:
            # Handle user profile update
            edit_form = UserEditForm(request.POST, instance=user)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('student_dashboard')
            else:
                messages.error(request, "Error updating profile. Please check your input.")

        elif 'upload_sheet' in request.POST:
            # Handle resume sheet upload
            upload_form = ResumeUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                answer_sheet = upload_form.save(commit=False)
                answer_sheet.user = user
                answer_sheet.save()
                messages.success(request, "Answer sheet uploaded successfully.")
                return redirect('student_dashboard')
            else:
                messages.error(request, "Error uploading resume  Please try again.")
        elif 'upload_answer_sheet' in request.POST:
            # Handle answer sheet upload
            upload_form = AnswerSheetUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                answer_sheet = upload_form.save(commit=False)
                answer_sheet.student = user
                answer_sheet.save()
                messages.success(request, "Answer sheet uploaded successfully.")
                return redirect('student_dashboard')
            else:
                messages.error(request, "Error uploading answer sheet. Please try again.")        
    else:
        edit_form = UserEditForm(instance=user)
        upload_form = ResumeUploadForm()
        answer_sheet_form = AnswerSheetUploadForm()

    context = {
        'user': user,
        'answer_sheets': resumes,
        'companies': companies,
        'scheduled_tests': scheduled_tests,
        'edit_form': edit_form,
        'upload_form': upload_form,
        'answer_sheet_form': answer_sheet_form,
    }
    return render(request, 'student_dashboard', context)

@login_required
def upload_answer_sheet(request, test_id):
    test = get_object_or_404(ScheduledTest, id=test_id)
    if request.method == 'POST':
        form = AnswerSheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            answer_sheet = form.save(commit=False)
            answer_sheet.test = test
            answer_sheet.student = request.user
            answer_sheet.save()
            messages.success(request, "Answer sheet uploaded successfully.")
        else:
            messages.error(request, "Error uploading answer sheet. Please try again.")
    return redirect('student_dashboard')

@login_required
def delete_resume(request, sheet_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=sheet_id)
        resume.file.delete()  # Delete the file from the storage
        resume.delete()  # Delete the record from the database
        messages.success(request, "Answer sheet deleted successfully.")
    else:
        messages.error(request, "Invalid request method.")
    return redirect(reverse('student_dashboard'))


@login_required
def company_dashboard(request):
    # Debug statement to print the email of the logged-in user
    print(f"Logged-in user's email: {request.user.email}")

    try:
        # Ensure the logged-in user is an instance of the Company model
        if not isinstance(request.user, Company):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('home')

        company = Company.objects.get(email=request.user.email)
    except Company.DoesNotExist:
        messages.error(request, "No Company matches the given query.")
        return redirect('home')

    # Debug statement to confirm the company object
    print(f"Company found: {company}")

    qualified_students = CustomUser.objects.filter(cgpa_or_percentage__gte=company.qualification_criteria)
    resumes = Resume.objects.filter(user__in=qualified_students)

    if request.method == 'POST':
        if 'create_test' in request.POST:
            test_form = TestCreationForm(request.POST)
            if test_form.is_valid():
                test = test_form.save(commit=False)
                test.company = company
                test.save()
                for student in qualified_students:
                    ScheduledTest.objects.create(student=student, company=company, test_date=test.test_date, description=test.description)
                messages.success(request, "Test created and scheduled for qualified students.")
                return redirect('company_dashboard')
        else:
            form = CompanyDashboardForm(request.POST, instance=company)
            if form.is_valid():
                form.save()
                messages.success(request, "Dashboard updated successfully!")
                return redirect('company_dashboard')
            test_form = TestCreationForm()  # Ensure test_form is initialized

    else:
        form = CompanyDashboardForm(instance=company)
        test_form = TestCreationForm()

    context = {
        'company': company,
        'students': qualified_students,
        'resumes': resumes,
        'form': form,
        'test_form': test_form,
    }
    return render(request, 'company_dashboard.html', context)

def schedule_test(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    company = Company.objects.first()  # Assuming the company is the one scheduling the test
    if not company:
        messages.error(request, "No company available to schedule the test.")
        return redirect('company_dashboard')
    test_date = company.test_date  # Assuming the test date is set in the company model
    description = "First round written test"

    ScheduledTest.objects.create(student=student, company=company, test_date=test_date, description=description)
    messages.success(request, f"Test scheduled for {student.username}.")
    return redirect('company_dashboard')
