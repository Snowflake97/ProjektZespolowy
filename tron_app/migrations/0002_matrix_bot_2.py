# Generated by Django 3.0.4 on 2020-04-27 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tron_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrix',
            name='bot_2',
            field=models.FileField(blank=True, upload_to='bots/'),
        ),
    ]
