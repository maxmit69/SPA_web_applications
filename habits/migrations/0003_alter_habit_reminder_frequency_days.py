# Generated by Django 5.0.6 on 2024-06-27 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_remove_habit_reminder_period_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='reminder_frequency_days',
            field=models.CharField(choices=[('mon', 'Понедельник'), ('tue', 'Вторник'), ('wed', 'Среда'), ('thu', 'Четверг'), ('fri', 'Пятница'), ('sat', 'Суббота'), ('sun', 'Воскресенье')], help_text='выберите дни недели для напоминаний о выполнении привычки (как минимум один день)', verbose_name='периодичность выполнения привычки в днях'),
        ),
    ]