# Generated by Django 5.1.7 on 2025-05-22 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='reciever',
            new_name='receiver',
        ),
    ]
