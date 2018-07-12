from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, PermissionsMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import UserAdminCreationForm
from .models import *

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)

    form = UserAdminCreationForm

    list_display = ('email', 'admin', 'is_active', 'staff')
    list_filter = ('admin', 'staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('first_name','last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active','user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Habiter)
admin.site.register(Etudiant)
admin.site.unregister(Group)
admin.site.register(Frequenter)
admin.site.register(Faculte)
admin.site.register(Ville_residence)
admin.site.register(Travailler)