# Generated by Django 3.0.8 on 2020-08-28 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0020_auto_20200820_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='occasion',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Occasion'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='payment',
            field=models.BooleanField(default=False, verbose_name='Payment'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone number'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='special_request',
            field=models.TextField(blank=True, null=True, verbose_name='Special Request'),
        ),
    ]
