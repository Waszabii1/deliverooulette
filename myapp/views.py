from django.shortcuts import render
from django.http import *
from .forms import Postcode, CuisineAsker, CuisinePicker
from .models import ToDoList, Item
from bs4 import BeautifulSoup

import requests

import random

# Create your views here.
postcode = ""
cuisine_choices = ""

def home(response): 
    return render(response, "home.html")

def clear_cuisine(request):
    cuisine_choices = ""  
    return render(request, "home.html")

def cuisine_asker(request):
    if request.method == "POST":
        cuisines = ["Afternoon tea","All day breakfast","American",
                    "Asian", "Asian Fusion","Breakfast","British", 
                    "Brunch", "Café", "Chinese", "French","Healthy", 
                    "Indian", "Italian", "Japanese", "Korean", 
                    "Lebanese", "Mediterranean", "Middle Eastern", "Thai", "Turkish"]
        return render(request, "want_cuisines.html", {"cuisines": cuisines})
    
    else:
        return render(request, 'home.html')

def cuisine_choices_func(request):
    if request.method == "POST":
        cuisine_choices = ""
        restaurants = {}
        groceries = {}
        cuisine_choicess = (request.POST.getlist("my_cuisine_list[]"))
        for i in cuisine_choicess:
            i = str(i).lower().replace(" ","+")
            cuisine_choices += f"&cuisine={i}"
        postcode = request.POST.get("Postcode")
        url_groceries = f'https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}&cuisine=grocery&collection=all-restaurants' #generates a list of grocery shops to remove
        result_groc = requests.get(url_groceries)
        doc_groc = BeautifulSoup(result_groc.text, "html.parser")
        tags_groc = doc_groc.find_all("a")

        for tag in range(5, (len(tags_groc) -28)):  # removes Nones and Social Medias, gets list of groceries

            place = tags_groc[tag].get("aria-label")

            url = tags_groc[tag].get("href")

            try:

                groceries.update({place : url})

            except TypeError:

                pass
            
               
        url_main = f'https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}{cuisine_choices}&collection=all-restaurants' #generates a list of all restaurants
        result_main = requests.get(url_main)
        doc_main = BeautifulSoup(result_main.text, "html.parser")
        tags_main = doc_main.find_all("a")

        for tag in range(5, (len(tags_main) - 28)):  # removes Nones and Social Medias, gets list of all places

            place = tags_main[tag].get("aria-label")

            url = tags_main[tag].get("href")

            try:

                restaurants.update({place : url})

            except TypeError:

                pass
            
        for val in groceries: #removes groceries from all restaurants
            if val in restaurants:
                restaurants.pop(val)                
                
        amount = len(restaurants)
        
        if amount == 0: #deals with index 0 errors and shows something if no restaurants avilable
            return render(request, "norest.html", {"postcode": postcode}) 
        rest = key, val = random.choice(list(restaurants.items()))
        output_rest = f"Out of {amount} restaurants, the random restaurant for {postcode} is {key}"
        output_url = f"https://deliveroo.co.uk{val}"
        restaurants.pop(key, val)
        request.session["postcode"] = postcode #gives postcode to reroll function
        request.session["restaurants"] = restaurants
        
        
        if amount == 1:
            return render(request, "1rest.html", {"restaurant": output_rest, "url" : output_url})
        else:
            return render(request, 'result.html', {"restaurant": output_rest, "url" : output_url})
        

def list_maker(request):
    restaurants = {}
    groceries = {}
    if request.method == "POST": #gets postcode, generates lists of restaurants
        postcode = request.POST.get("Postcode")
        url_groceries = f'https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}&cuisine=grocery&collection=all-restaurants' #generates a list of grocery shops to remove
        result_groc = requests.get(url_groceries)
        doc_groc = BeautifulSoup(result_groc.text, "html.parser")
        tags_groc = doc_groc.find_all("a")

        for tag in range(5, (len(tags_groc) -28)):  # removes Nones and Social Medias, gets list of groceries

            place = tags_groc[tag].get("aria-label")

            url = tags_groc[tag].get("href")

            try:

                groceries.update({place : url})

            except TypeError:

                pass
            
               
        url_main = f'https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}{cuisine_choices}&collection=all-restaurants' #generates a list of all restaurants
        result_main = requests.get(url_main)
        doc_main = BeautifulSoup(result_main.text, "html.parser")
        tags_main = doc_main.find_all("a")

        for tag in range(5, (len(tags_main) - 28)):  # removes Nones and Social Medias, gets list of all places

            place = tags_main[tag].get("aria-label")

            url = tags_main[tag].get("href")

            try:

                restaurants.update({place : url})

            except TypeError:

                pass
            
        for val in groceries: #removes groceries from all restaurants
            if val in restaurants:
                restaurants.pop(val)                
                
        amount = len(restaurants)
        
        if amount == 0: #deals with index 0 errors and shows something if no restaurants avilable
            return render(request, "norest.html", {"postcode": postcode}) 
        rest = key, val = random.choice(list(restaurants.items()))
        output_rest = f"Out of {amount} restaurants, the random restaurant for {postcode} is {key}"
        output_url = f"https://deliveroo.co.uk{val}"
        restaurants.pop(key, val)
        request.session["postcode"] = postcode #gives postcode to reroll function
        request.session["restaurants"] = restaurants
        
        
        if amount == 1:
            return render(request, "1rest.html", {"restaurant": output_rest, "url" : output_url})
        else:
            return render(request, 'result.html', {"restaurant": output_rest, "url" : output_url})
        
        
    else:
        return render(request, 'home.html')

def re_roll(request):
    restaurants = request.session["restaurants"]
    if request.method == "POST":
        postcode = request.session["postcode"]
        amount = len(restaurants)
        no_rest_url = f"https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}&collection=all-restaurants"
        if amount == 0:
            return render(request, "norest.html", {"url":no_rest_url})
        rest = key, val = random.choice(list(restaurants.items()))
        output_rest = f"Out of {amount} restaurants, the random restaurant for {postcode} is {key}"
        output_url = f"https://deliveroo.co.uk{val}"
        restaurants.pop(key, val)
        if amount == 1:
            return render(request, "1rest.html", {"restaurant": output_rest, "url" : output_url})
        else:
            return render(request, 'result.html', {"restaurant": output_rest, "url" : output_url})
        
        
    else:
        return render(request, 'home.html')

