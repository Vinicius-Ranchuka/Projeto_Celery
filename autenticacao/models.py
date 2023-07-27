from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

#Os itens adicionados aos models Token e UsuariosTemporarios são temporários e são deletados após 30 minutos, apenas os itens registrados no Usuarios é permanente, isso foi feito porque usuários sem email confirmado não são interessantes para o projeto
    
class Token(models.Model):
    token = models.CharField(max_length=100)
    hora_inscricao = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.token
class UsuariosTemporarios(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    caminho_convite = models.CharField(max_length=200, null=True)
    hora_inscricao = models.DateTimeField(default= timezone.now)
    def __str__(self):
        return self.nome
class Usuarios(AbstractUser):
    caminho_convite = models.CharField(max_length=200)
    def __str__(self):
        return self.username

class DataAtual(models.Model):
    data_atual = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.data_atual)