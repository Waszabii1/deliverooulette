from django import forms

class Postcode(forms.Form):
    PostCode = forms.CharField(label="Postcode", max_length=8)
    
    
class Cuisine_Picker(forms.Form):
    Check = forms.BooleanField()