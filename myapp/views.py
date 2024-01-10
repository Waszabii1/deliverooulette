from django.shortcuts import render
from django.http import *
from .forms import Postcode, CuisineAsker, CuisinePicker
from .models import ToDoList, Item
from bs4 import BeautifulSoup

import requests

import random

# Create your views here.

def home(response): 
    return render(response, "home.html", {"name":"test"})

def list_maker(request):
    restaurants = {}
    groceries = {}
    cuisine_choices = ""
    if request.method == "POST":
        postcode = request.POST.get("Postcode")
        url_main = f'https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}{cuisine_choices}&collection=all-restaurants'
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
    
        url_groceries = f'https://deliveroo.co.uk/restaurants/london/westminster?postcode={postcode}&cuisine=grocery&collection=all-restaurants'
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
        
        return render(request, 'result.html', {"restaurants": restaurants})
    else:
        return render(request, 'home.html')

def download_file(request):
    if 'scraped_data' in request.session:
        context = request.session['scraped_data']
        response = HttpResponse(content_type='')
        if request.POST['download_type'] == 'pdf':
            template_path = 'result.html'
            template = get_template(template_path)
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            filename = f"{context['title']}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
            if pisa_status.err:
                return HttpResponse('PDF generation failed')
        elif request.POST['download_type'] == 'csv':
            response = HttpResponse(content_type='text/csv')
            filename = f"{context['title']}.csv"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            writer = csv.writer(response)
            writer.writerow(['Title', 'Headings', 'Paragraphs'])
            rows = zip([context['title']], context['headings'], context['paragraphs'])
            for row in rows:
                writer.writerow(row)
        elif request.POST['download_type'] == 'json':
            response = HttpResponse(content_type='application/json')
            filename = f"{context['title']}.json"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            json.dump(context, response, indent=4)
        return response
    else:
        return render(request, 'home.html')