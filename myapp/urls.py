from django.urls import path
from .import views

urlpatterns = [
    path("", views.myview, name = "test"),
    path("", views.test_form, name="form")
]