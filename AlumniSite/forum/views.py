from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView, FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from forum.models import Groupe, Appartenir, Subject, Comment, Request
from forum.forms import FormGroup, SubjectForm
from main.models import Evenement
from main.forms import EventForm
from forum.decorators import can_access
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

User = get_user_model()

class IndexCommunity(TemplateView):
    template_name = 'forum/community.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Groupe.objects.filter(activated=True)
        return context


class ListViewGroup(ListView):
    model = Groupe
    context_objects_name = 'groups'
    template_name = 'forum/groupes.html'
    queryset = Groupe.objects.filter(activated=True)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class CreateGroupeView(LoginRequiredMixin,CreateView):
    template_name = 'forum/group_form.html'
    form_class = FormGroup
    success_url = reverse_lazy('forum:community')

    def form_valid(self, form):
        form.instance.activated = True
        self.object = form.save()
        print(self.object)
        new_appart = Appartenir(
            admin = True,
            group = self.object,
            alumni = self.request.user,
        )
        new_appart.save()
        print(new_appart)
        return super().form_valid(form)

    def form_invalid(self,form):
        print(form.errors)
        return super().form_invalid(form)

class DetailsViewGroup(LoginRequiredMixin,DetailView):
    template_name = 'forum/list_subject.html'
    model = Groupe
    context_object_name = 'group'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_groups'] = Appartenir.objects.get_app_by_user(self.request.user)
        return context 


class DetailsViewSubject(LoginRequiredMixin, DetailView):
    template_name = 'forum/details_subject.html'
    model = Subject
    context_object_name = 'subject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_groups'] = Appartenir.objects.get_app_by_user(self.request.user)
        return context 

def addSubject(request):
    if request.method == 'GET':
        group_id = request.GET.get('group')
        content = request.GET.get('content')
        group = get_object_or_404(Groupe, pk=group_id)
        new_subject = Subject(
            alumni = request.user,
            content = content,
            group= group
        )
        new_subject.save()
        html_context = get_template('forum/subjects.html').render({'group':Subject.objects.all()})
        if new_subject:
            data = {
                'ok':True,
                'html_context':html_context
            }
        return JsonResponse(data)

@login_required
def appendComments(request):
    if request.method == 'GET':
        subject_id = request.GET.get('subject')
        content = request.GET.get('content')

        subject = get_object_or_404(Subject, pk=subject_id)
        new_comment = Comment(
            subject = subject,
            content = content,
            alumni = request.user
        )
        new_comment.save()

        if new_comment:
            data = {
                'ok':True
            }
        return JsonResponse(data)
        
class ListGroupCommunity(LoginRequiredMixin, ListView):
    model = Groupe
    context_object_name = 'groups'
    template_name = 'forum/list_group.html'
    queryset = Groupe.objects.filter(activated=True)
    paginate_by = '3'

@login_required
def deleteSubject(request):
    if request.method=='GET':
        id = request.GET.get('id')
        subject = get_object_or_404(Subject, pk=id)
        subject.delete()
        data = {'ok':True}
        return JsonResponse(data)

class ManageGroup(LoginRequiredMixin, TemplateView,SingleObjectMixin, FormView):
    template_name = 'forum/manage_group.html'
    form_class = EventForm
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(pk=self.request.user.id)
        return context

class DeleteGroup(LoginRequiredMixin, DeleteView):
    template_name = 'forum/delete_group_confirm.html'
    model = Groupe
    context_object_name = 'object'

@login_required
def addRequest(request):
    ok = False
    
    if request.method=='GET':
        
        id = request.GET.get('id')
        
        group = get_object_or_404(Groupe, id=id)
        request_ = Request(
            alumni = request.user,
            group = group
        )
        request_.save()
        if request_:
            ok = True
        
    data = {'ok':ok}
    
    return JsonResponse(data)

class ListRequest(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'forum/list_request.html'
    context_object_name = 'requests'

@login_required
def acceptRequest(request, pk):
    if request.method == 'GET':
        request_ = get_object_or_404(Request, id=pk)
        app = Appartenir(
            group = request_.group,
            alumni = request_.alumni
        )
        app.save()
        if app:
            request_.delete()
        
    return redirect('forum:list_request')

@login_required
def declineRequest(request, pk):
    if request.method == 'GET':
        request_ = get_object_or_404(Request, id=pk)
        request_.delete()
    return redirect('forum:list_request')

@login_required
def quitGroup(request, pk):
    if request.method == 'GET':
        group = get_object_or_404(Groupe, pk=pk)
        
        app = get_object_or_404(Appartenir, group=group, alumni=request.user)
        if len(group.get_members()) == 1:
            group.delete()
        else:
            app_ = get_object_or_404(Appartenir, group=group, alumni=group.get_members()[1])
            app_.admin = True
            app_.save()
            
        app.delete()

        
    return redirect('forum:community')

@login_required
def deleteEvent(request):
    ok= False
    if request.method == 'GET':
        pk = request.GET.get('id')
        event = get_object_or_404(Evenement, pk=pk)
        event.delete()
        ok = True
    data = {
        'ok':ok
    }
    return JsonResponse(data)

            