from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core import serializers
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from accounts.models import *
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from main.forms import ActualiteForm, EventForm, ProjectForm
from main.models import Actualite, Evenement, Project, Contribution
from forum.models import Groupe, Appartenir
from forum.forms import FormGroup
from django.contrib.auth.decorators import user_passes_test
import json

User = get_user_model()


class IndexView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('admin_login:login')
    template_name = 'admin/index.html'

    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etudiants'] = Etudiant.objects.all()
        context['admins'] = User.objects.get_staff_user()
        context['users'] = User.objects.get_user(stat=True)
        context['suspend_users'] = User.objects.get_user(stat=False)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_admin:
                return HttpResponseRedirect(self.login_url)
        return super().get(request, *args, **kwargs)

class AjaxRequestAddUser(View):
    
    template = 'admin/activate_confirm.html'

    def get(self,request, *args, **kwargs):
        etudiant = get_object_or_404(Etudiant, pk=request.GET.get('pk'))
        #LogEntry(user=self.request.user, )
        
        self.make_migrations(etudiant)
        data = {
            'ok':True,
            'etudiants':Etudiant.objects.all().count(),
            'users':User.objects.filter(admin=False).count()
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

        profile = UserProfile(
            user = new_user,
            residence = etudiant.residence,
            matricule = etudiant.matricule,
            faculte = etudiant.faculte,
            diplome = etudiant.diplome,
            entreprise = etudiant.entreprise,
            fonction = etudiant.fonction,
            entree = etudiant.entree,
            telephone = etudiant.telephone
        )
        profile.save()

        if etudiant.faculte:
            admin = False
            try:
                group = Groupe.objects.get(name=etudiant.faculte)
                group.activated = True
                
                if group.get_admins():
                    admin = True
                app = Appartenir(group = group, alumni=new_user, admin=admin)
                group.save()
                app.save()
            except:
                print("pas de faculte en ce nom")
            
        send_mail_( self.request, new_user, self.template)
        
        etudiant.delete()

class ListViewUser(ListView):
    model = User
    context_object_name = "users"
    template_name = "admin/users_list.html"
    
    queryset = User.objects.filter(admin=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class CreateNews(CreateView):
    template_name = "admin/news_form.html"
    form_class = ActualiteForm
    success_url = reverse_lazy('admin:index')
    def form_valid(self, form):
        form.instance.image_description = self.get_form_kwargs().get('files')['image_description']
        form.instance.nb_vues = 0
        if len(form.instance.text_description) == 0:
            return super().form_invalid(form)
        form.save()
        return super(CreateNews, self).form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

def ajaxDeleteRequest(request):
    template = 'admin/activate_rejet.html'

    ok = False
    if request.method == 'GET':
        etudiant = Etudiant.objects.get(pk=request.GET.get('pk')).delete()
        
        ok = True
    data = {
        'ok':ok,
        'request_registration':Etudiant.objects.all().count(),
        'users_count':User.objects.all().count()
    }
    send_mail_(request, etudiant, template)
    return JsonResponse(data)

def ajaxSuspendRequest(request):
    ok = False
    if request.method == 'GET':
        user = get_object_or_404(User, pk=request.GET.get('pk'))
        user.is_active = False
        user.save()
        ok = True
    data = {
        'ok':ok,
        'suspend_user':User.objects.filter(is_active=False).count(),
        'users_count':User.objects.all().count()
    }
    return JsonResponse(data)

def ajaxActiveRequest(request):
    ok = False
    if request.method == 'GET':
        user = get_object_or_404(User, pk=request.GET.get('pk'))
        user.is_active = True
        user.save()
        ok = True
    data = {
        'ok':ok,
        'suspend_user':User.objects.filter(is_active=False).count(),
        'users_count':User.objects.all().count()
    }
    return JsonResponse(data)

class ChangeStateUser(View):

    http_method_names = ['get', 'put']

    ok = False

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.GET.get('pk'))
        user.is_active = False
        user.save()
        data = {'ok':True}
        return JsonResponse(data)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.PUT.get('pk'))
        user.is_active = False
        suer.save()
        data = {'ok':True}
        return JsonResponse(data)

class StatsView(TemplateView):
    template_name = 'admin/statistiques.html'

class ListEventsView(ListView):
    model = Evenement
    template_name = "admin/list_events.html"
    context_object_name = "events"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

def getUsers(request):
    users = User.objects.all()
    data = dict(users)
    return JsonResponse(data)


def send_mail_(request, user, template):

    current_site = get_current_site(request)

    context_ = {
        'user': user,
        'domain': current_site.domain,
    }
    print(context_)
    subject = "Activation accounts"
    to_email = user.email
    messages = get_template(template).render(context_)
    try:
        send_mail(
            subject,
            messages,
            from_email = settings.DEFAULT_FROM_EMAIL,
            recipient_list = [to_email]
        )
    except:
        print("the email activation can't been send")

class ListNews(ListView):
    model = Actualite
    context_object_name = 'news'
    template_name = 'admin/list_news.html'

class UpdateNewsView(UpdateView):
    model = Actualite
    form_class = ActualiteForm
    template_name = "admin/news_form.html"
    success_url = reverse_lazy('admin:index')

    def get_initial(self):
        initial = super(UpdateNewsView, self).get_initial()
        new = super().get_object()
        initial['title'] = new.title
        initial['author'] = new.author
        initial['text_description'] = new.text_description
        initial['image_description'] = new.image_description
        print(initial)
        print()
        return initial

class DeleteNewsView(DeleteView):
    model = Actualite
    template_name = 'admin/delete_confirm.html'
    context_object_name = 'object'
    success_url = reverse_lazy('admin:list_news')

class DeleteEventsView(DeleteView):
    model = Evenement
    template_name = 'admin/delete_confirm.html'
    context_object_name = 'object'
    success_url = reverse_lazy('admin:manage_events')

def eventActivation(request):
    ok = False
    if request.method == 'GET':
        pk = request.GET.get('pk')
        event = get_object_or_404(Evenement, pk=pk)
        event.activated = True
        event.save()

        ok = True
    data = {
            'ok':ok
        }
    return JsonResponse(data)

class AddProject(LoginRequiredMixin, CreateView):
    template_name = 'admin/add_project.html'
    form_class = ProjectForm
    success_url = reverse_lazy('admin:list_project')

    def form_valid(self, form):
        form.instance.add_by = self.request.user
        if self.request.user.is_admin:
            form.instance.activated = True
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class ListProject(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'admin/list_project.html'
    context_object_name = 'projects'

class DonateList(ListView):
    model = Contribution
    template_name = 'admin/donate_confirm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contributions'] = Contribution.objects.filter(confirmed=False)
        context['donates'] = Contribution.objects.filter(confirmed=True)
        return context

def confirmDonate(request):
    ok = False
    if request.method=='GET':
        id = request.GET.get('id')
        contribution = get_object_or_404(Contribution, pk=id)
        contribution.confirmed = True
        contribution.save()
        if contribution:
            ok=True
    data = {
        'ok':ok
    }
    return JsonResponse(data)

def projectActivation(request):
    ok = False
    if request.method == 'GET':
        pk = request.GET.get('pk')
        project = get_object_or_404(Project, pk=pk)
        project.activated = True
        project.save()

        ok = True
    data = {
            'ok':ok
        }
    return JsonResponse(data)

class AddGroup(LoginRequiredMixin, CreateView):
    template_name = 'admin/group_form.html'
    form_class = FormGroup
    success_url = reverse_lazy('admin:list_group')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class ListGroup(LoginRequiredMixin, ListView):
    model = Groupe
    template_name = 'admin/list_group.html'
    context_object_name = 'groupes'

class DetailsProject(LoginRequiredMixin,DeleteView):
    model = Project
    template_name = 'admin/details_project.html'
    context_object_name = 'project'