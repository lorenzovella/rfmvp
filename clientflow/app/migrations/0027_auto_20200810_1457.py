# Generated by Django 3.0.8 on 2020-08-10 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20200802_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plano',
            options={'ordering': ['-last_updated']},
        ),
    ]