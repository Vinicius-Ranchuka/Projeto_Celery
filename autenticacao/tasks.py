from time import sleep
from celery import shared_task
from django.utils import timezone
from .models import UsuariosTemporarios, Token, DataAtual
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
import os
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from hashlib import sha256
from django.conf import settings
#Apaga dados dos bancos temporários de mais de um dia atrás
def apagar_bancos_temporarios():
    tempo_limite = timezone.now() - timedelta(days=1)
    UsuariosTemporarios.objects.filter(hora_inscricao__lt=tempo_limite).delete()
    Token.objects.filter(hora_inscricao__lt=tempo_limite).delete()

@shared_task
def minha_tarefa():
    sleep(10)
    return 'teste'

#criando a imagem personalizada

def img_personaliazada(usuario_temporario):
    caminho_convite = os.path.join(settings.STATIC_ROOT, 'img/convite.png')
    print(caminho_convite)
    imagem = Image.open(caminho_convite)

    # Converter para o modo RGB
    imagem = imagem.convert("RGB")
    desenho = ImageDraw.Draw(imagem)
    nome = usuario_temporario.nome
    fonte = ImageFont.truetype(os.path.join(settings.STATIC_ROOT, "img/fontes/arial.ttf"), 20)
    
    posicao_texto = (115, 30)
    desenho.text(posicao_texto, nome, font=fonte, fill=(0, 0, 0))

    email= usuario_temporario.email
    posicao_texto = (125, 125)
    desenho.text(posicao_texto, email, font=fonte, fill=(0, 0, 0))

    # caminho_area_de_trabalho = os.path.expanduser('~/Área de Trabalho/')
    chave_secreta = 'ODmgsdppv?aǵ,$4oGDM_#_ADGk04g@+23r'
    token = sha256((chave_secreta + str(usuario_temporario.id)).encode()).hexdigest()
    caminho_salvar = os.path.join(settings.MEDIA_ROOT, f'convites/{token}.png')
    imagem.save(caminho_salvar)
    return token
@shared_task(bind=True,max_retries=10,default_retry_delay=2,
            #  auto_retry_for=(Exception,),retry_backoff = True,retry_backoff_max = 600,retry_jitter = False
             )
def mandar_email(self,usuario_temporario_id):
    try:
        #filtrando os dados necessários
        usuario_temporario = UsuariosTemporarios.objects.filter(id=usuario_temporario_id)[0]
        token = Token.objects.filter(id=usuario_temporario.token_id)[0]
        
        #gera a o convite e retorna o token do convite
        token_convite = img_personaliazada(usuario_temporario)
        
        #gerando o link de confirmação
        link_confirmacao = 'http://127.0.0.1:8000'+ reverse('confirm_email', args=[usuario_temporario_id,token])

        caminho_convite = f'/media/convites/{token_convite}.png'
        #salvando o caminho do convite no banco de dados para poder acessá-lo depois
        usuario_temporario.caminho_convite = caminho_convite
        usuario_temporario.save()
        
        #configurações do email
        html_content = render_to_string('cadastro/emails/email.html', {'nome':usuario_temporario.nome, 'token_convite': token_convite, 'link_confirmacao':link_confirmacao,'caminho_convite':caminho_convite})
        text_content = strip_tags(html_content)
        assunto_email = 'Verificação de email'
        remetente = settings.EMAIL_HOST_USER
        destinatarios = [usuario_temporario.email]
        #aplicando as configurações
        email = EmailMultiAlternatives(
        assunto_email,
        text_content,
        remetente,
        destinatarios
        )
        email.attach_alternative(html_content, 'text/html')
        #enviando o email
        email.send()
    except Exception as e:
        self.retry(countdown=2**self.request.retries)

@shared_task(bind=True)
def atualiza_horario(self):
    data_atual = DataAtual.objects.all().first()
    data_atual.data_atual = timezone.now()
    data_atual.save()
    return 'Done '