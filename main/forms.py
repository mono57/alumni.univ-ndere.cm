from django import forms
from .models import Evenement, Actualite, Project
import datetime

class EventForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'description','image_illustration' ,'lieu', 'date_evenement','heure_debut', 'heure_fin']
        widgets = {
            "titre" : forms.TextInput(attrs={'class':'form-control'}),
            "description" : forms.Textarea(attrs={'class':'form-control'}),
            "image_illustration" : forms.FileInput(attrs={'class':'form-control'}),
            "lieu" : forms.TextInput(attrs={'class':'form-control'}),
            "date_evenement" : forms.DateInput(attrs={'class':'form-control datepicker'}),
            "heure_debut" : forms.TimeInput(attrs={'class':'form-control timepicker'}),
            "heure_fin" : forms.TimeInput(attrs={'class':'form-control timepicker'}),
        }

    def clean(self):
        clean_data = super(EventForm, self).clean()
        date_ = clean_data.get('date_evenement')
        titre = clean_data.get('titre')

        try:
            event = Evenement.objects.get(titre=titre)
        except:
            event = None
        if event is not None:
            self.add_error('titre','Ce titre a été déjà pris. S\'il vous plait choisissez un autre')

        if date_ < datetime.date.today():
            self.add_error('date_evenement', 'La date de l\'événement est incorrecte')
        return clean_data

class ActualiteForm(forms.ModelForm):
    class Meta:
        model = Actualite
        fields = '__all__'

    def clean(self):
        clean = super(ActualiteForm, self).clean()
        text_description = clean['text_description']
        if len(text_description) == 0:
            self.add_error('text_description', 'La description ne peut pas être vide')

        return clean

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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'time', 'execute', 'montant']

    def clean(self):
        clean_data = super(ProjectForm, self).clean()
        name = clean_data['name']
        try:
            project = Project.objects.get(name=name)
        except:
            project = None

        if project is not None:
            self.add_error('name', 'Le nom du projet existe déjà')

        return clean_data