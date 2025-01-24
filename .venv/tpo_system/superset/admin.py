from django.contrib import admin
from .models import Company
from .models import CustomUser
# Register your models here.
admin.site.register(CustomUser)



class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'qualification_criteria', 'date_of_visit', 'application_deadline']

admin.site.register(Company, CompanyAdmin)
