from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Evenement, Actualite
from main.forms import CreateEventForm, ContactForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView):
    template_name = 'home_page.html'

class ListActualite(ListView):
    template_name = 'main/liste_actu.html'
    context_object_name = 'actualites'
    model = Actualite

class DetailNews(DetailView):
    model = Actualite
    template_name = 'main/details_news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = Actualite.objects.all()[:5]
        return context

class ListEvenement(ListView):
    template_name = 'main/liste_event.html'
    context_object_name = 'evenements'
    model = Evenement


@login_required(login_url='login')
def create_event(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_event = Evenement(
                titre=form.cleaned_data['titre'],
                description = form.cleaned_data['description'],
                lieu = form.cleaned_data['lieu'],
                image_description = form.cleaned_data['image_description'],
                date_evenement = form.cleaned_data['date_evenement'],
                createur = request.user
            )
            new_event.save()
            print("Enregistrement effectué avec succès")
            return redirect('main:liste_event')
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
