from django.urls import path
from .views import submit_contact_form

app_name = 'home'

urlpatterns = [
    path('submit-contact/', submit_contact_form, name='submit_contact_form'),
]
