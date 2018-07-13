from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from accounts.models import *
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from main.forms import ActualiteForm
from main.models import Actualite

User = get_user_model()

def get_staff_user():
    return User.objects.filter(admin=True) 

class IndexView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('admin_login:login')
    template_name = 'admin/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etudiants'] = Etudiant.objects.all()
        context['admins'] = get_staff_user()
        context['users'] = User.objects.all()[:5]
        context['habitations'] = Habiter.objects.all()
        context['user_not_active'] = self.get_suspend_user()

        return context

    def get_suspend_user(self):
        return User.objects.filter(is_active=False).count()

class AjaxRequestAddUser(View):
    def get(self,request, *args, **kwargs):
        try:
            etudiant = Etudiant.objects.get(pk=request.GET.get('pk'))
        except:
            print('Error')
        if etudiant:
            self.make_migrations(etudiant)
        data = {
            'etudiants':Etudiant.objects.all()
        }
        return JsonResponse(data)

    def make_migrations(self,etudiant):
        new_user = User.objects.create_user(
            first_name=etudiant.prenom,
            last_name=etudiant.nom,
            email=etudiant.email,
            password=etudiant.mot_de_passe
        )
        new_user.save()

        new_faculte = Faculte(
            nom = etudiant.faculte
        )
        new_faculte.save()

        new_frequenter = Frequenter(
            matricule = etudiant.matricule,
            annee_entree = etudiant.annee_entree,
            annee_sortie = etudiant.annee_sortie,
            dernier_diplome = etudiant.diplome,
            user = new_user,
            faculte = new_faculte
        )
        new_frequenter.save()

        new_ville = Ville_residence(
            nom = etudiant.residence
        )
        new_ville.save()

        new_entreprise = Entreprise(
            nom = etudiant.entreprise
        )
        new_entreprise.save()

        new_habiter = Habiter(
            ville = new_ville,
            user = new_user
        )
        new_habiter.save()

        new_travailler = Travailler(
            fonction = etudiant.fonction,
            user = new_user,
            entreprise = new_entreprise 
        )
        new_travailler.save()
        
        etudiant.delete()

class ListViewUser(ListView):
    model = User
    context_object_name = "users"
    template_name = "admin/users_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admins'] = get_staff_user()
        return context

class CreateNews(CreateView):
    template_name = "admin/news_form.html"
    form_class = ActualiteForm
    success_url = reverse_lazy('admin:index')
    def form_valid(self, form):
        form.instance.image_description = self.get_form_kwargs().get('files')['image_description']
        form.save()
        return super(CreateNews, self).form_valid(form)

    def form_invalid(self, form):
        print("le formulaire n'est pas valide")
        print(self.get_form_kwargs())
        print(form.errors)
        return super().form_invalid(form)
