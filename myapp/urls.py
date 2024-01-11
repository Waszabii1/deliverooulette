from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("rand_rest/", views.list_maker, name="rand_rest"),
    path("cuisine_asker/", views.cuisine_asker, name="cuisine_asker"),
    path("cuisine_choices/", views.cuisine_choices_func, name="cuisine_choices_func"),
    path("clear_cuisine/", views.clear_cuisine, name="clear_cuisine"),
    path("reroll/", views.re_roll, name="reroll")
]