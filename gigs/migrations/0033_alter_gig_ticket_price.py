# Generated by Django 5.1.7 on 2025-06-12 19:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gigs', '0032_alter_gig_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='ticket_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=5.0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
