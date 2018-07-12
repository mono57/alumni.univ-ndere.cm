from django.shortcuts import render
from django.views.generic import TemplateView

class IndexCommunity(TemplateView):
    template_name = 'forum/community.html'
