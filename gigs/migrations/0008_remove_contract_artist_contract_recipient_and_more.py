# Generated by Django 5.1.7 on 2025-04-10 19:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0007_gig_is_public'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='artist',
        ),
        migrations.AddField(
            model_name='contract',
            name='recipient',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contracts_as_recipient', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contracts_as_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
