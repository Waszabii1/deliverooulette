from django.shortcuts import render
from django.http import *


# Create your views here.

def myview(request): 
    return render(request, "index.html")

def test_form(request):   
    if request.method == "POST":
        user = request.POST.get('username')
        if user == "mark":
            return HttpResponse('hello mark')
        
def cuisine_choice_getter(request):
    some_var = request.POST.getlist("checks")