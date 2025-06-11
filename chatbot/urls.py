# chatbot/urls.py
from django.urls import path
from .views import chatbot_view
from .views import suggest_symptoms
from .views import chatbot_view, appointment_chatbot_view
urlpatterns = [
    path('chat/', chatbot_view, name='chatbot-text'),
    path('suggest/', suggest_symptoms, name='chatbot-suggest'),
    path("appointment/", appointment_chatbot_view, name="chatbot-appointment"),
    

]
