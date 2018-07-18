from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from forum.models import Groupe

class IndexCommunity(TemplateView):
    template_name = 'forum/community.html'


class ListViewGroup(ListView):
    model = Groupe
    context_objects_name = 'groups'
    template_name = 'forum/groupes.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)