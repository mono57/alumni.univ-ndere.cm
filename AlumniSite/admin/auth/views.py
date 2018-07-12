from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView
from django.urls import reverse_lazy

class LoginAdmin(FormView):
    form_class = AuthenticationForm
    template_name = 'admin/auth/login.html'
    success_url = reverse_lazy('admin:index')

    def form_valid(self, form):
        
        return super().form_valid(form)