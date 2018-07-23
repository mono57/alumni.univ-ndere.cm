from django import forms
from forum.models import Groupe


class GroupeForm(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = '__all__'
        