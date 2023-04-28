from django.urls import path

from . import views

urlpatterns = [
    path("aadhar_upload", views.aadhar_upload, name="aadhar"),
    path("gate_upload", views.gate_upload, name="gate"),
]