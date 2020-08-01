# Generated by Django 3.0.8 on 2020-08-01 23:12

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20200731_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='sabores',
        ),
        migrations.AddField(
            model_name='cachorro',
            name='sabores',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Carne de panela', 'Carne de panela'), ('Frango Xadrez', 'Frango Xadrez'), ('Risoto Suíno', 'Risoto Suíno')], default='', max_length=42, verbose_name='Escolha os sabores do futuro'),
        ),
    ]
