# Generated by Django 5.0.6 on 2024-05-31 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_checkin_data_checkout_quarto_checkin_quarto_hospede_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='endereco',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='telefone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
