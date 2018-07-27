from django.views.generic import TemplateView, ListView, CreateView, DetailView, View
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Evenement, Actualite, Comment
from main.forms import CreateEventForm, ContactForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


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
        context['news'] = Actualite.objects.all()
        context['events'] = Evenement.objects.all()
        context['first_event'] = Evenement.objects.first()
        return context

class ListActualite(ListView):
    template_name = 'main/liste_actu.html'
    context_object_name = 'news'
    model = Actualite

class DetailNews(DetailView):
    model = Actualite
    template_name = 'main/details_news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = Actualite.objects.all()[:3]
        context['events'] = Evenement.objects.all()[:3]
        
        return context

class ListEvenement(ListView):
    template_name = 'main/liste_event.html'
    context_object_name = 'evenements'
    model = Evenement

class DetailEvent(DetailView):
    model = Evenement
    template_name = 'main/detail_event.html'
    context_object_name = 'evenement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_events'] = Evenement.objects.all()[:5]
        
        return context

@login_required(login_url='login')
def create_event(request):
    
    if request.method == 'POST':
        form = CreateEventForm(request.POST or None, request.FILES or None)
        print(request.FILES)
        if form.is_valid():
            new_event = Evenement(
                titre=request.POST.get('titre'),
                description = request.POST.get('description'),
                lieu = request.POST.get('lieu'),
                image_illustration = request.FILES.get('image_illustration'),
                date_evenement = request.POST.get('date_evenement'),
                heure_debut = request.POST.get('heure_debut'),
                heure_fin = request.POST.get('heure_fin'),
                createur = request.user
            )
            print(form.cleaned_data)
            new_event.save()
            print("Enregistrement effectué avec succès")
            return redirect('event')
        else:
            print(request.POST)
            print(request.FILES)
            print(form.errors)
            print('le formulaire n est pa valide')
    form = CreateEventForm()
    context = {'form':form}
    return render(request, 'main/create_event.html', context)


class CreateEventView(CreateView,LoginRequiredMixin):
    form_class = CreateEventForm
    template_name = 'main/create_event.html'
    success_url = reverse_lazy('main:liste_event')

    def form_valid(self, form):

        return super().form_valid(form)

class ContactView(FormView):
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('/')
    form_class = ContactForm

    def form_valid(self,form):
        return super().form_valid(form)


class ProjectsView(TemplateView):
    template_name = "main/projects.html"

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
