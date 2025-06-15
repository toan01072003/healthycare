from django.urls import path
from . import views
from vitals import views as vitals_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),  # Thêm route home tại đây
    path('profile/', views.profile_view, name='profile'),
    path('nurse/', views.nurse_home_view, name='nurse-home'),
    path('nurse/patients/', views.nurse_patient_list_view, name='nurse-patient-list'),
    path('nurse/patients/<uuid:patient_id>/', views.nurse_patient_detail_view, name='nurse-patient-detail'),
    path('nurse/patients/<uuid:patient_id>/add-vital/', vitals_views.add_vital_for_patient_view, name='nurse-add-vital'),
    path('lab/', views.lab_home_view, name='lab-home'),
]
