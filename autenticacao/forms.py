from .models import Usuarios
from django.contrib.auth import forms

#sobrescrevendo os dados do User para conseguirmos maior autonomia
class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = Usuarios

class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Usuarios

#Formulário da página de cadastro
class FormCliente(forms.forms.Form):
    nome = forms.forms.CharField(max_length=30)
    email = forms.forms.EmailField()

    def __init__(self,*args,**keyargs):
        super().__init__(*args,**keyargs)  
        self.fields['nome'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] ='form-control'

