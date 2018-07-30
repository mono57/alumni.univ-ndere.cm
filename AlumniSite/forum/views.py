from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from forum.models import Groupe, Appartenir, Subject
from forum.forms import FormGroup
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexCommunity(TemplateView):
    template_name = 'forum/community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Groupe.objects.all()
        return context


class ListViewGroup(ListView):
    model = Groupe
    context_objects_name = 'groups'
    template_name = 'forum/groupes.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class CreateGroupeView(LoginRequiredMixin,CreateView):
    template_name = 'forum/group_form.html'
    form_class = FormGroup
    success_url = reverse_lazy('forum:community')

    def form_valid(self, form):
        self.object = form.save()
        print(self.object)
        new_appart = Appartenir(
            groupe = self.object,
            alumni = self.request.user
        )
        new_appart.save()
        return super().form_valid(form)

    def form_invalid(self,form):
        print(form.errors)
        return super().form_invalid(form)

class DetailsViewGroup(LoginRequiredMixin,DetailView):
    template_name = 'forum/group_details.html'
    model = Groupe

def addSubject(request):
    if request.method == 'GET':
        group_id = request.GET.get('group')
        content = request.GET.get('content')
        group = get_object_or_404(Groupe, pk=group_id)
        new_subject = Subject()
        new_subject.alumni = request.user
        new_subject.content = content

        new_subject.save()

        new_subject.group.add(group)
        
        if new_subject:
            data = {
                'ok':True
            }
        return JsonResponse(data)