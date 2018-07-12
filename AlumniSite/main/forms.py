from django import forms
from .models import Evenement, Actualite

class CreateEventForm(forms.Form):
    titre = forms.CharField(max_length=200,
         widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''})
    )
    description = forms.CharField(
        widget = forms.Textarea(attrs={'class':'form-control', 'placeholder':''})
    )
    lieu = forms.CharField(max_length=30,
     widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':''})
     )
    image_illustration = forms.FileField(
        widget=forms.FileInput(attrs={'class':'form-control'})
    )
 
class ActualiteForm(forms.ModelForm):
    class Meta:
        model = Actualite
        fields = '__all__'

class ContactForm(forms.Form):
    nom = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'class':'col-md-6 norightborder', 'placeholder':'Votre nom*'})
    )
    email = forms.EmailField(max_length=30,
        widget=forms.EmailInput(attrs = {'class':'col-md-6 norightborder','placeholder':'Votre adresse email*'})
    )
    message = forms.CharField(max_length=100,
        widget=forms.Textarea(attrs = {'class':'col-md-12 norightborder', 'placeholder':'Message*'})
    )   