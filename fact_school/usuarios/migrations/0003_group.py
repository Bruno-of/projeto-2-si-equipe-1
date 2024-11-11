# Generated by Django 5.1.1 on 2024-11-10 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_remove_category_criterion_remove_category_max_score_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('members', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='usuarios.user')),
            ],
        ),
    ]
