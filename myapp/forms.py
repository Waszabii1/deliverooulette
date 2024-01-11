from django import forms

class CuisineAsker(forms.Form):
    check = forms.BooleanField(required=False)

class Postcode(forms.Form):
    postcode = forms.CharField(label="Please enter a valid postcode", max_length=8,)
    
    
class CuisinePicker(forms.Form):
    cuisines = forms.BooleanField(required=False)
