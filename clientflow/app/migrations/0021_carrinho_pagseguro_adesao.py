# Generated by Django 3.0.8 on 2020-07-30 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_carrinho_pagseguro_plano'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='pagseguro_adesao',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
    ]