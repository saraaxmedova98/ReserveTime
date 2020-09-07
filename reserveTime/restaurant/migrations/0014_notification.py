# Generated by Django 3.0.8 on 2020-08-14 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0013_comment_comment_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('read', models.BooleanField(default=False, verbose_name='Read')),
                ('notified_at', models.DateTimeField(verbose_name='Notification date')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_notification', to='restaurant.Company', verbose_name='Company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
