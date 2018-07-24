from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, TemplateView, CreateView
from django.contrib.auth.models import User
from accounts.forms import LoginForm, EtudiantForm, CustomPasswordResetForm
from accounts.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login, get_user_model
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

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
            user = authenticate(request, email=email, password = password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
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

class ProfileAccountView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travailler'] = Travailler.objects.filter(user=self.request.user)
        context['frequenter'] = Frequenter.objects.filter(user=self.request.user)
        context['habiter'] = Habiter.objects.filter(user=self.request.user)
        return context

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