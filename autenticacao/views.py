from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .tasks import minha_tarefa, mandar_email
from .forms import FormCliente
from django.urls import reverse
import secrets
from django.contrib import messages
from django.contrib.messages import constants
from .models import Token, UsuariosTemporarios, Usuarios
from django.utils import timezone

def home(request):
    minha_tarefa.delay() 
    #adicionar o botão para ir para o cadastro
    return HttpResponse('<h1>Estou na home</h1>')

def cadastro(request):
    if request.method == 'GET':
        form = FormCliente()     
        for i in form.fields.keys():
            placeholder = ''
            if i == 'nome':
                placeholder = 'Digite seu nome...'
            elif i == 'email':
                placeholder = 'Digite seu email...'
            form.fields[i].widget.attrs['placeholder'] = placeholder
        return render(request, 'cadastro/cadastro.html', {'form': form})
    elif request.method == 'POST':
        form = FormCliente(request.POST)
        if form.is_valid():
            nome_cadastro = form.data['nome']
            email_cadastro = form.data['email']
            # form.cleaned_data
            
            if  Usuarios.objects.filter(email=email_cadastro).exists():
                messages.add_message(request, constants.ERROR, 'Já existe uma pessoas cadastrada com esse nome')
                return redirect('/cadastro/')
            
            #gerando o token para possibilitar a verificação do email
            token_confimacao = secrets.token_urlsafe(16)
            token = Token(token=token_confimacao, hora_inscricao=timezone.now())
            token.save()

            usuario_temporario = UsuariosTemporarios(nome=nome_cadastro,email=email_cadastro,token_id=token.id, hora_inscricao=timezone.now())
            usuario_temporario.save()
            return redirect(f'/cadastrando_pessoa/{usuario_temporario.id}')

        else:
            messages.add_message(request, constants.WARNING, 'Digite nome e email válidos')
            return redirect('/cadastrando_pessoa/')

# personaliza a imagem com as informações do usuário


def confirm_email(request,usuario_temporario_id,token):
        # try:
            if Token.objects.get(token=token):
                usuario_temporario = UsuariosTemporarios.objects.filter(id=usuario_temporario_id)[0]
                usuario = Usuarios.objects.create_user(username=usuario_temporario.nome,email=usuario_temporario.email, caminho_convite=usuario_temporario.caminho_convite)
                usuario.is_active = True
                usuario.save()
                link = reverse('cadastro_realizado', args=[usuario.id])

                messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
                return redirect(link)
            else:
                messages.add_message(request, constants.ERROR, 'Falha ao verificar o email')
                return redirect('/cadastro/')
        # except:
        #     messages.add_message(request, constants.ERROR, 'Falha ao verificar o email')
        #     return redirect('/cadastro/')
def cadastrando_pessoa(request,usuario_temporario_id):
    mandar_email.delay(usuario_temporario_id)
    return render(request, 'cadastro/cadastrando_pessoa.html')

def cadastro_realizado(request, usuario_id):
    caminho_convite = Usuarios.objects.filter(id=usuario_id)[0].caminho_convite
    return render(request, 'cadastro/cadastro_realizado.html', {'caminho_convite':caminho_convite })

