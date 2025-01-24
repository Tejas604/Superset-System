from django.contrib.auth.models import AbstractUser 
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
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
    cgpa_or_percentage = models.CharField(max_length=10, blank=True, null=True)  # CGPA or percentage

    previous_place_of_work = models.CharField(max_length=255, blank=True, null=True)  # Previous work details
    achievements = models.TextField(blank=True, null=True)  # Achievements details
    positions_of_responsibility = models.TextField(blank=True, null=True)  # Positions of responsibility

    # Change default username field to email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # Username is still required for creating a user
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email

class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="resumes/")

    def __str__(self):
        return f"{self.user.email} - {self.file.name}"
   
    def file_url(self):
        return self.file.url


class CompanyManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        company = self.model(email=email, **extra_fields)
        company.set_password(password)
        company.save(using=self._db)
        return company

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class Company(AbstractBaseUser, PermissionsMixin):
    OPPORTUNITY_TYPE_CHOICES = [
        ('Placement', 'Placement'),
        ('Internship', 'Internship'),
        ('I+P', 'Internship + Placement'),
    ]
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    qualification_criteria = models.DecimalField(max_digits=4, decimal_places=2, help_text="Minimum CGPA", default=6.6)
    job_description = models.FileField(upload_to='job_descriptions/', null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE_CHOICES, default='Placement')
    duration = models.CharField(max_length=50, null=True, blank=True, help_text="Duration (e.g., '6 months')")
    hiring_stages = models.TextField(help_text="List the hiring stages (e.g., Aptitude, Technical Interview, HR Interview)", default="Not specified")
    role = models.CharField(max_length=255, help_text="Job Role (e.g., Software Engineer, Intern)")
    date_of_visit = models.DateField(help_text="Date when the company will visit")
    application_deadline = models.DateField(help_text="Last date for application submission", default="2025-01-01")
    test_date = models.DateField(help_text="Date for the test", null=True, blank=True)
    interview_date = models.DateField(help_text="Date for the interview", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='company_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='company_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    objects = CompanyManager()

    def __str__(self):
        return self.name
    
class ScheduledTest(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    test_date = models.DateField(help_text="Date for the test")
    description = models.TextField(help_text="Description of the test")

    def __str__(self):
        return f"Test for {self.student.username} by {self.company.name} on {self.test_date}"

# Test model    
class Test(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    test_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.company.name} - Test on {self.test_date}"    

class AnswerSheet(models.Model):
    test = models.ForeignKey(ScheduledTest, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="answer_sheets/")

    def __str__(self):
        return f"{self.student.username} - {self.file.name}"