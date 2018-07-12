from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Evenement, Actualite
from main.forms import CreateEventForm, ContactForm
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'home_page.html'

class ListActualite(ListView):
    template_name = 'main/liste_actu.html'
    context_object_name = 'actualites'
    model = Actualite

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
                acces = form.cleaned_data['acces'], 
                image_illustration = form.cleaned_data['image_illustration'],
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


class CreateEventView(CreateView):
    form_class = CreateEventForm
    model = Evenement
    template_name = 'main/create_event.html'
    success_url = reverse_lazy('event')

    def form_valid(self, form):
        
        form.instance.createur = self.request.user
        form.save()
        return HttpResponseRedirect(self.get_success_url())

class ContactView(FormView):
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('/')
    form_class = ContactForm

    def form_valid(self,form):
        return super().form_valid(form)
