from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.utils.timezone import now
from .forms import CustomUserRegistrationForm
from .models import CustomUser, AnswerSheet, Company


def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()  # Save the user to the database
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


def home(request):
    return render(request, 'home.html')


# Forms for editing and uploading
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'work_experience', 'projects', 'certifications',
            'educational_qualification', 'educational_description',
            'previous_place_of_work', 'achievements', 'positions_of_responsibility'
        ]


class AnswerSheetUploadForm(forms.ModelForm):
    class Meta:
        model = AnswerSheet
        fields = ['file']


@login_required
def student_dashboard(request):
    """View to manage the student dashboard."""
    user = request.user
    answer_sheets = AnswerSheet.objects.filter(user=user)
    companies = Company.objects.filter(date_of_visit__gte=now().date()).order_by('date_of_visit')

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
            # Handle answer sheet upload
            upload_form = AnswerSheetUploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                answer_sheet = upload_form.save(commit=False)
                answer_sheet.user = user
                answer_sheet.save()
                messages.success(request, "Answer sheet uploaded successfully.")
                return redirect('student_dashboard')
            else:
                messages.error(request, "Error uploading answer sheet. Please try again.")
    else:
        edit_form = UserEditForm(instance=user)
        upload_form = AnswerSheetUploadForm()

    context = {
        'user': user,
        'answer_sheets': answer_sheets,
        'companies': companies,
        'edit_form': edit_form,
        'upload_form': upload_form,
    }
    return render(request, 'student_dashboard', context)
