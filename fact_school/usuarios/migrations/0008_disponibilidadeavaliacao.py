# Generated by Django 5.0.1 on 2024-12-06 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_remove_relatorioavaliacao_media_delete_respostafact'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisponibilidadeAvaliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio', models.DateTimeField()),
                ('fim', models.DateTimeField()),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disponibilidades', to='usuarios.turma')),
            ],
        ),
    ]
