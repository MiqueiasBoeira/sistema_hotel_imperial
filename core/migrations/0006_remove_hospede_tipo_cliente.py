# Generated by Django 5.0.6 on 2024-07-07 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_quarto_checkin_remove_checkout_checkin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospede',
            name='tipo_cliente',
        ),
    ]