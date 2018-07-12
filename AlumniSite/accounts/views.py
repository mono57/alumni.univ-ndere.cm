from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, TemplateView, CreateView
from django.contrib.auth.models import User
from accounts.forms import LoginForm, EtudiantForm, CustomPasswordResetForm
from accounts.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('passwords:password_reset_done')

class CustomPasswordResetViewDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('passwords:password_reset_complete')

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password = password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            messages.info(request, "Vos identifiants de connexion sont incorrects. Veuillez réessayer.")
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'accounts/login.html', context)

class CreateEtudiant(CreateView):
    template_name = 'accounts/register.html'
    form_class = EtudiantForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        return super().form_valid(form)

class ProfileAccountView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['travailler'] = Travailler.objects.get(user=self.request.user)
        context['frequenter'] = Frequenter.objects.get(user=self.request.user)
        context['habiter'] = Habiter.objects.get(user=self.request.user)
        return context