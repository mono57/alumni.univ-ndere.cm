from django.views.generic import TemplateView, ListView, CreateView, DetailView, View, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Evenement, Actualite, Comment, Project, Contribution, Inscription
from main.forms import EventForm, ContactForm, ProjectForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
import datetime


class HomePageView(TemplateView):
    template_name = 'home_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Actualite.objects.all()
        return context

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = Actualite.objects.all()[:3]
        context['events'] = Evenement.objects.filter(activated=True)[:3]
        return context

class ListActualite(ListView):
    template_name = 'main/liste_actu.html'
    context_object_name = 'news'
    model = Actualite
    paginate_by = 6

class DetailNews(DetailView):
    model = Actualite
    template_name = 'main/details_news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = Actualite.objects.exclude(id=self.object.id)[:3]
        context['events'] = Evenement.objects.filter(activated=True)[:3]
        
        return context
    

class ListEvenement(ListView):
    template_name = 'main/liste_event.html'
    context_object_name = 'evenements'
    model = Evenement
    queryset = Evenement.objects.get_activated_events()
    paginate_by = 5

class DetailEvent(DetailView):
    model = Evenement
    template_name = 'main/detail_event.html'
    context_object_name = 'evenement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_events'] = Evenement.objects.exclude(id=self.object.id)[:3]
        return context

class CreateEventView(LoginRequiredMixin,CreateView):
    form_class = EventForm
    template_name = 'main/create_event.html'
    success_url = reverse_lazy('event')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "Création d'evénement"
        return context

    def form_valid(self, form):
        form.instance.createur = self.request.user
        form.save()
        return super().form_valid(form)


class UpdateEventView(LoginRequiredMixin,UpdateView):
    form_class = EventForm
    template_name = 'main/create_event.html'
    model = Evenement
    success_url = reverse_lazy('event')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "Modification d'un evénement"
        context['title'] = "Modification"
        return context

    def form_valid(self, form):
        form.instance.createur = self.request.user
        form.save()
        return super().form_valid(form)
        
class ContactView(FormView):
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('/')
    form_class = ContactForm

    def form_valid(self,form):
        return super().form_valid(form)


class ProjectsView(LoginRequiredMixin, ListView):
    template_name = "main/projects.html"
    model = Project
    context_object_name = 'projects'
    queryset = Project.objects.filter(activated=True)

class AddComment(View):
        
    def get(self, request):
        new = get_object_or_404(Actualite, pk=request.GET.get('pk'))
        new_comment = Comment(
            author = request.GET.get('author'),
            email = request.GET.get('email'),
            website = request.GET.get('website'),
            text = request.GET.get('text'),
            new = new
        )
        new_comment.save()
        data = {
            'ok':True,
        }
        return JsonResponse(data)

class DetailsProject(DetailView):
    model = Project
    template_name = 'main/details_project.html'
    context_object_name = 'project'
    queryset = Project.objects.filter(activated=True)
    paginate_by = 1

class MakeSuggestion(CreateView):
    form_class = ProjectForm
    template_name = 'main/suggest_project_form.html'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.instance.add_by = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

def addContribution(request):
    ok = False
    if request.method=='GET':
        id = request.GET.get('project')
        montant = request.GET.get('montant')
        project = get_object_or_404(Project, pk=id)
        new_contribution = Contribution(
            alumni = request.user,
            montant = montant,
            project = project,
            mode_payement = request.GET.get('mode')
        )
        new_contribution.save()

        if new_contribution:
            ok = True
    data = {
        'ok':ok
    }
    return JsonResponse(data)

@login_required
def eventRegister(request):
    ok = False
    if request.method=='GET':
        id = request.GET.get('id')
        evenement = get_object_or_404(Evenement, pk=id)
        inscription = Inscription(
            alumni = request.user,
            event = evenement
        )
        inscription.save()

        if inscription:
            ok = True
    data = {
        'ok':ok
    }
    return JsonResponse(data)