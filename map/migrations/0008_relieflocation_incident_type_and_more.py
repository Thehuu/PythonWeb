# Generated by Django 5.1.3 on 2024-12-19 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_incident'),
    ]

    operations = [
        migrations.AddField(
            model_name='relieflocation',
            name='incident_type',
            field=models.CharField(choices=[('traffic_accident', 'Tai nạn giao thông'), ('drowning', 'Đuối nước'), ('fire', 'Cháy'), ('natural_disaster', 'Thiên tai')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='relieflocation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
