# Generated by Django 5.1.7 on 2025-04-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0008_alter_user_profileimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='artist_logo'),
        ),
    ]
