# Generated by Django 3.0.8 on 2020-07-22 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200722_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cachorroespecial',
            name='anexo',
            field=models.URLField(blank=True, help_text='Clique ou arraste os arquivos nessa área para anexá-los', null=True, verbose_name='Algum exame ou receita?'),
        ),
    ]