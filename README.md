# Projeto_Celery
### Neste projeto, desenvolvi um website que simula uma plataforma de venda de cursos, exigindo que o usuário forneça seu nome e e-mail para ter acesso à aula gratuita, a qual o convida para participar do curso.

## Pré-requisitos

- Python 3.x
- Broker(Redis recomendado)

## Instalação do Broker

### No Linux:
- Abra terminal e rode os comandos `sudo apt-get update` e `sudo apt-get upgrade` para atualizar todos os pacotes do sistema
- Digite o comando `sudo apt install redis` para instalar o Redis
- Verifique se a versão está atualizada com o comando `redis-cli --version`
- Reestarte o Redis para ter certeza que ele está rodando com o seguinte comando `sudo service redis restart`
- Rode o comando `redis-cli` e digite `ping`, se o retorno for `PONG`, o redis está rodando corretamente

### No Windows:

Siga as instruções do tutorial abaixo:

[![Vídeo de como instalar Redis no Windows](https://github.com/Vinicius-Ranchuka/Projeto_Celery/blob/master/imagens_ilustrativas/thumbnail_tutorial.jpg)](https://www.youtube.com/watch?v=5VZpzwJeMDo "Vídeo de como instalar Redis no Windows")

## Baixando o repositório
- Clique em `Code`(ou código caso esteja traduzido)
- Baixe em Zip(ou da forma de sua prefência) e descompacte aonde quiser.

## Instalações Gerais
- Abra o terminal, e entre na pasta `p_celery-master`
- Crie o `venv`(ambiente virtual) com os seguintes comandos:  
    1)Linux: `python3 -m venv venv`  
    2)Windows: `python -m venv venv`
  
- Ative o ambiente virtual:  
  1)Linux: `source venv/bin/activate`    
  2)Windows: `venv\Scripts\Activate`  

  Caso algum comando retorne um erro de permissão execute o código e tente novamente:
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

- Com o `venv` ativo execute o código `pip install -r requirements.txt`(cerifique-se que `requirements.txt` esteja em `p_celery-master`), isso vai instalar as bibliotecas de código que foram usadas no projeto.

## Configurações  

Esse projeto faz envio de emails e para que o projeto funcione corretamente é necessário que personalize os dados no settings.py conforme requisitado.
![imagem do settings.py](https://github.com/Vinicius-Ranchuka/Projeto_Celery/blob/master/imagens_ilustrativas/configurar_email.png)

### Como criar uma senha de app?

- Vá em 'gerenciar sua conta Google'
- Pesquise por 'senhas de app'
- Selecione o app Email e personalise um nome para essa senha de app
  ![Senha de app](https://github.com/Vinicius-Ranchuka/Projeto_Celery/blob/master/imagens_ilustrativas/senha_app.png)
    
- Clique em gerar, copie o código e cole na variável `senha_email`

- Inicie o servidor local:
    1)Linux: `python3 manage.py runserver`
    2)Windows: `python manage.py runserver`

- Inicie o Worker com o comando `celery -A core worker`
  
## Tudo Configurado!  
Agora é só acessar `http://127.0.0.1:8000/cadastro/` e testar o site.
