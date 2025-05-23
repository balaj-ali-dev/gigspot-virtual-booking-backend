# Generated by Django 5.1.7 on 2025-03-27 18:15

import custom_auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0007_user_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profileImage',
            field=models.ImageField(blank=True, default=None, null=True, upload_to=custom_auth.models.user_profile_image_path),
        ),
    ]
