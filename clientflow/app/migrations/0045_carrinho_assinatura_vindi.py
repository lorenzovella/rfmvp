# Generated by Django 3.1.1 on 2020-11-18 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_remove_carrinho_status_adesao'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='assinatura_vindi',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]
