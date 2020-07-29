from accounts.forms import LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from admin.auth.decorators import admin_only
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test


def login(request):
    
    error = False
    not_permission = True
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(request, email=data['email'], password=data['password'])
        if user is not None:
            print(user)
            if user.is_admin:
                auth_login(request, user)
                return redirect('admin:index')
            not_permission = True
        else:
            error = True
    context = {
        'not_permission':not_permission,
        'error':error,
        'form':form
    }
    return render(request, 'admin/auth/login.html', context)
            
    
