# Generated by Django 4.2.15 on 2024-10-06 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_relieflocation_created_at_relieflocation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='relieflocation',
            name='mobile',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
