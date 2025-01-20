from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    work_experience = models.TextField(blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    educational_qualification_12th = models.CharField(max_length=255, blank=True, null=True)
    educational_qualification_degree = models.CharField(max_length=255, blank=True, null=True)
    previous_place_of_work = models.CharField(max_length=255, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    positions_of_responsibility = models.TextField(blank=True, null=True)
