# Generated by Django 5.1.1 on 2024-12-05 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_relatorioavaliacao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relatorioavaliacao',
            old_name='justificativa',
            new_name='justificativas',
        ),
    ]