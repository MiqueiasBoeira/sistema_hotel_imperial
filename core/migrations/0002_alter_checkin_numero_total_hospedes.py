# Generated by Django 5.0.6 on 2024-06-02 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='numero_total_hospedes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
