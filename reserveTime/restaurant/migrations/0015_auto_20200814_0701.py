# Generated by Django 3.0.8 on 2020-08-14 07:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0014_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='company',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='reciever',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reciever_notification', to=settings.AUTH_USER_MODEL, verbose_name='Company'),
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender_notification', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
