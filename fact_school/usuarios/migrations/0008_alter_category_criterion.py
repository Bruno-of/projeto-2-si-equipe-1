# Generated by Django 5.1.3 on 2024-11-23 02:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_grupo_turma_remove_studentresponse_criterion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='criterion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='usuarios.criterion'),
        ),
    ]
