from django.shortcuts import render
from django.http import *
from .forms import Postcode

# Create your views here.

def index(reponse): 
    return render(response, "index.html")

def test_form(reponse):
    postcode = Postcode()
    return render(response,"forms.html", {"form":postcode})