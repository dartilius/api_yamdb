# Generated by Django 3.2 on 2023-04-27 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор'), ('superuser', 'Суперпользователь')], default='user', max_length=31, verbose_name='Роль'),
        ),
    ]