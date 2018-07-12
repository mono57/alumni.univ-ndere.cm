from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Frequenter, Etudiant
from django.contrib.auth.forms import PasswordResetForm 

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.clean_data.get('password1')
        password2 = self.clean_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas')
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'


class LoginForm(forms.Form):
    email = forms.CharField(max_length=255,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse de connexion'})
    )
    password = forms.CharField(max_length=100,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Mot de passe'})
    )
    remember = forms.BooleanField(required=False,
        widget=forms.CheckboxInput(attrs={'class':'form-check-input'})
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        max_length=User._meta.get_field('email').max_length,
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )