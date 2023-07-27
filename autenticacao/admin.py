from django.contrib import admin
from .models import Token,UsuariosTemporarios,Usuarios,DataAtual
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth import admin as admin_auth_django
# Register your models here.
admin.site.register(Token)
admin.site.register(UsuariosTemporarios)
admin.site.register(DataAtual)

@admin.register(Usuarios)
class UsersAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Usuarios
    