from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastrando_pessoa/<int:usuario_temporario_id>', views.cadastrando_pessoa, name='cadastrando_pessoa'),
    path('confirm_email/<int:usuario_temporario_id>/<str:token>/', views.confirm_email, name='confirm_email'),
    path('cadastro_realizado/<int:usuario_id>', views.cadastro_realizado, name='cadastro_realizado'),
  
]
