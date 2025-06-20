# Generated by Django 5.1.7 on 2025-06-18 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0032_merge_20250618_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venue',
            name='tier',
        ),
        migrations.AlterField(
            model_name='artist',
            name='subscription_tier',
            field=models.CharField(choices=[('FREE', 'Free'), ('PREMIUM', 'Premium')], default='FREE', help_text='Subscription level for premium features', max_length=50),
        ),
        migrations.AlterField(
            model_name='venue',
            name='amenities',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='venue',
            name='capacity',
            field=models.IntegerField(default=0),
        ),
    ]
