# Generated by Django 5.1.1 on 2024-11-29 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_remove_avaliacaofact_equipe_remove_avaliacaofact_fim_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipe',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipes', to='usuarios.turma'),
        ),
    ]
