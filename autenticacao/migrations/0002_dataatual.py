# Generated by Django 4.2.2 on 2023-07-19 22:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataAtual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_atual', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]