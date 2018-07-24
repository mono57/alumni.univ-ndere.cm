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

    def clean(self):
        clean_data = super(EtudiantForm, self).clean()
        faculte = clean_data['faculte']
        matricule = clean_data['matricule']
        annee_entree = clean_data.get('annee_entree')
        if User.objects.filter(email=clean_data['email']).exists():

            self.add_error('email', "this email is already taken")

        if matricule and Frequenter.objects.filter(matricule=matricule).exists():
            self.add_error('matricule', 'This matricule is already exist')

        if not matricule:
            if not faculte and not annee_entree:
                self.add_error("matricule","Failing registration enter your faculty and year of entry")

            if faculte and not annee_entree or not faculte and annee_entree:
                self.add_error("matricule","Failing registration please read the registration conditions")
        return clean_data


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