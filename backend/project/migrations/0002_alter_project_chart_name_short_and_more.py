# Generated by Django 5.0.4 on 2024-04-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='chart_name_short',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Коротка назва для тв-програми'),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_production',
            field=models.DateField(blank=True, null=True, verbose_name='дата релізу'),
        ),
    ]
