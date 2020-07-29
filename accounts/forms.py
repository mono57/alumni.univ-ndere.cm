from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Frequenter, Etudiant, UserProfile
from django.contrib.auth.forms import PasswordResetForm 
from django.core.files.images import get_image_dimensions

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
            self.add_error('password1','Les mots de passe ne correspondent pas')
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

            self.add_error('email', "Cette adresse email a été déjà prise")

        if matricule and UserProfile.objects.filter(matricule=matricule).exists():
            self.add_error('matricule', 'Ce matricule existe déjà')

        if not matricule:
            if not faculte and not annee_entree:
                self.add_error("matricule","À defaut du matricule entrez l'établissement et l'année d'entrée")

            if faculte and not annee_entree or not faculte and annee_entree:
                self.add_error("faculte","À defaut du matricule entrez l'établissement et l'année d'entrée")
        return clean_data


class LoginForm(forms.Form):
    email = forms.CharField(max_length=255,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse de connexion'})
    )
    password = forms.CharField(max_length=100,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Mot de passe'})
    )
    remember = forms.BooleanField(required=False,initial=True,
        widget=forms.CheckboxInput(attrs={'class':'form-control pull-left'})
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        max_length=User._meta.get_field('email').max_length,
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )

class UserProfileForm(forms.Form):
    residence = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    matricule = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    faculte = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    dernier_diplome = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    entreprise = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    fonction = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    annee_universitaire = forms.DateField(required=False,widget=forms.DateInput(attrs={'class':'form-control'}))
    avatar = forms.ImageField(required=False)
    telephone = forms.IntegerField(required=False)   

    def clean_avatar(self):
        clean_data = super().clean()
        avatar = clean_data['avatar']

        try:
            width, height = get_image_dimensions(avatar)
            max_width = max_height = 100
            if width > max_width or height > max_height:
                self.add_error('avatar',"La taille de l'image choisie est trop grande")

            if len(avatar) > 100*1024:
                self.add_error('avatar',"La taille du fichier ne peut pas depasser 100K")
        except:
            print("Une erreur est survenue")       

        return avatar