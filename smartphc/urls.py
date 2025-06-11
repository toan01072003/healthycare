"""
URL configuration for smartphc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user-profile/', include('user_profile.urls')),
    path('doctor/', include('appointment.urls')), 
    
    path('api/medical-record/', include('medical_record.urls')),
    path('api/symptom-checker/', include('symptom_checker.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/prescription/', include('prescription.urls')),
    path('api/vitals/', include('vitals.urls')),
    path('api/chronic-care/', include('chronic_care.urls')),
    path('api/lab/', include('lab.urls')),
    path('api/pharmacy/', include('pharmacy.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/admin-management/', include('admin_management.urls')),
    path('auth/', include('auth_service.urls')),  

    path('', TemplateView.as_view(template_name='login_register.html')),
]
