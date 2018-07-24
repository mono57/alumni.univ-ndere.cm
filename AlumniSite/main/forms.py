from django import forms
from .models import Evenement, Actualite

class CreateEventForm(forms.Form):
    class Meta:
        model = Evenement
        fields = ['titre', 'description','image_illustration' ,'lieu', 'date_evenement','heure_debut', 'heure_fin']
 
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