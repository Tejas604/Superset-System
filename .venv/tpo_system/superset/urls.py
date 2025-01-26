from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('delete_sheet/<int:sheet_id>/', views.delete_resume, name='delete_sheet'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('company-register/', views.company_register, name='company_register'),
    path('company-dashboard/', views.company_dashboard, name='company_dashboard'),
    path('schedule_test/<int:student_id>/', views.schedule_test, name='schedule_test'),
    path('upload_answer_sheet/<int:test_id>/', views.upload_answer_sheet, name='upload_answer_sheet'),
    path('create_test/', views.company_dashboard, name='create_test'),
    
]
if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
