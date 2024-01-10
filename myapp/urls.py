from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("forms/", views.list_maker, name="form")
]