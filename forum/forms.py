from django import forms
from forum.models import Groupe, Subject


class FormGroup(forms.ModelForm):
    class Meta:
        model = Groupe
        fields = ['name', 'description', 'category', 'status', 'avatar']
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['content']