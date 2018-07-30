from django import forms
from forum.models import Groupe


class FormGroup(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = '__all__'
        