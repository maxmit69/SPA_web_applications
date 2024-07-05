# Generated by Django 5.0.6 on 2024-06-27 17:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habit',
            name='reminder_period_days',
        ),
        migrations.AddField(
            model_name='habit',
            name='reminder_frequency_days',
            field=models.IntegerField(default=1, help_text='Периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)], verbose_name='Периодичность выполнения привычки в днях'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='time_start_habits',
            field=models.TimeField(help_text='введите время начала привычки', verbose_name='время начала привычки'),
        ),
    ]
