from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, DetailView, TemplateView, CreateView, UpdateView
from django.contrib.auth.models import User
from accounts.forms import LoginForm, UserProfileForm, CustomPasswordResetForm, EtudiantForm
from accounts.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login, get_user_model
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('passwords:password_reset_done')

class CustomPasswordResetViewDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('passwords:password_reset_complete')

class LoginView(FormView):

    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

def login_page(request):
    error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember = request.POST.get('remember')
            user = authenticate(request, email=email, password = password)
            
            if user is not None:
                auth_login(request, user)
                request.session['user_id'] = user.id
                if not remember:
                    del request.session['user_id']
                return redirect(request.POST.get('next') or 'index')
            error = True
    else:
        form = LoginForm()


    context = {
        'form':form,
        'error': error
    }
    return render(request, 'accounts/login.html', context)

class CreateEtudiant(CreateView):
    template_name = 'accounts/register.html'
    form_class = EtudiantForm
    success_url = reverse_lazy('accounts:registration_send')

    def form_valid(self, form): 
        print(form.cleaned_data)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.cleaned_data)
        print()
        print(form.errors)
        return super().form_invalid(form)

class ProfileAccountView(UpdateView):
    template_name = 'accounts/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_form(self, form_class=UserProfileForm):
        self.object = self.get_object()
        profile = self.object
        form = form_class(
            initial={
                'residence' : profile.residence,
                'matricule' : profile.matricule,
                'faculte' : profile.faculte,
                'dernier_diplome' : profile.diplome,
                'entreprise' : profile.entreprise,
                'fonction' : profile.fonction,
                'annee_universitaire' : profile.entree,
                'avatar':profile.avatar,
                'telephone':profile.telephone
            }
        )
        return form

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, 'accounts/profile.html', {'form':form})
    
    def form_valid(self, form):
        data  = form.cleaned_data
        profile = self.get_object()
        profile = profile.update_profile(data)
        if profile:
            print('le profils a été mis a jour')
        return HttpResponseRedirect(self.get_object().get_absolute_url())

    
   

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken':User.objects.filter(email=email).exists()
    }
    return JsonResponse(data)

class RegistrationSend(TemplateView):
    template_name = 'accounts/registration_send.html'

class RegistrationConditions(TemplateView):
    template_name = 'accounts/accounts_conditions.html'