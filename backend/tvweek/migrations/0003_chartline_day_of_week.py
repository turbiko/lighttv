# Generated by Django 5.0.4 on 2024-04-10 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvweek', '0002_alter_chartline_program_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartline',
            name='day_of_week',
            field=models.IntegerField(blank=True, null=True, verbose_name='День тижня (1-Пн,7-Нд'),
        ),
    ]
