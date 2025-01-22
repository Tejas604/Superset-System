from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Required fields for authentication
    email = models.EmailField(unique=True)  # Unique email for authentication
    password = models.CharField(max_length=128)  # Default password field from AbstractUser

    # Work and education fields
    WORK_EXPERIENCE_CHOICES = [
        ('Fresher', 'Fresher'),
        ('1-2 Years', '1-2 Years'),
        ('3-5 Years', '3-5 Years'),
        ('5+ Years', '5+ Years'),
    ]
    work_experience = models.CharField(
        max_length=20,
        choices=WORK_EXPERIENCE_CHOICES,
        blank=True,
        null=True
    )
    projects = models.TextField(blank=True, null=True)  # Projects details
    certifications = models.TextField(blank=True, null=True)  # Certifications details

    # Educational qualification with choices
    EDUCATION_LEVEL_CHOICES = [
        ('10th', '10th'),
        ('12th', '12th'),
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
        ('PhD', 'PhD'),
    ]
    educational_qualification = models.CharField(
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        blank=True,
        null=True
    )
    educational_description = models.TextField(
        blank=True,
        null=True,
        help_text="Add any specific details about your education (e.g., board, percentage, etc.)"
    )

    previous_place_of_work = models.CharField(max_length=255, blank=True, null=True)  # Previous work details
    achievements = models.TextField(blank=True, null=True)  # Achievements details
    positions_of_responsibility = models.TextField(blank=True, null=True)  # Positions of responsibility

    # Change default username field to email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Username is still required for creating a user

    def __str__(self):
        return self.email

class AnswerSheet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="answer_sheets/")

    def __str__(self):
        return f"{self.user.email} - {self.file.name}"


class Company(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    eligibility_criteria = models.TextField()
    date_of_visit = models.DateField()

    def __str__(self):
        return self.name