# Generated by Django 3.0.8 on 2020-08-02 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20200802_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrega',
            name='frequencia',
            field=models.IntegerField(choices=[(1, ' 1 Entrega no mês (Grátis)'), (2, '2 Entregas no mês (R$9,90)')], default=0, verbose_name='Com qual frequência quer receber a Ração do Futuro?'),
        ),
    ]
