import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf.settings',namespace='CELERY')

#configuração das tarefas
app.conf.beat_schedule = {
    'apagar_dados_temporarios': {
        'task': 'autenticacao.tasks.apagar_bancos_temporarios',
        'schedule': crontab(hour=4,minute=20),#executa a tarefa todo dia ás 4:20 da manhã 
    },
    'atualiza_horario':{
        'task': 'autenticacao.tasks.atualiza_horario',
        'schedule': crontab()#executa a cada minuto
    }
}


