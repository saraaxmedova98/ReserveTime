# Generated by Django 3.0.8 on 2020-08-17 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0017_comment_overall'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='cover_photo',
            field=models.ImageField(blank=True, null=True, upload_to='company-photos/', verbose_name='Photo'),
        ),
    ]
