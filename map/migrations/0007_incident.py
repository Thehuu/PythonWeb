# Generated by Django 5.1.3 on 2024-12-15 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0006_relieflocation_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_type', models.CharField(choices=[('TNGT', 'Tai nạn giao thông'), ('DROWNING', 'Đuối nước'), ('FIRE', 'Cháy'), ('DISASTER', 'Thiên tai')], max_length=10)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]