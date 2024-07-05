from django.db import models
from django.core.exceptions import ValidationError
from users.models import NULLABLE


class Habit(models.Model):
    WEEK_DAYS = (
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    )
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец привычки')
    place = models.CharField(max_length=225, verbose_name='место выполнения привычки',
                             help_text='введите место выполнения привычки')
    time_start_habits = models.TimeField(verbose_name='время начала привычки',
                                         help_text='формат заполнения: ЧЧ:ММ:СС', )
    action = models.CharField(max_length=150, verbose_name='действие привычки',
                              help_text='введите действие которое выполняет привычка')
    pleasant_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки',
                                         help_text='выберите, если привычку можно отнести к приятной привычке')
    linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE,
                                     help_text='введите связанную привычку для полезных привычек')
    reminder_frequency_days = models.CharField(
        choices=WEEK_DAYS,
        verbose_name='периодичность выполнения привычки в днях',
        help_text='выберите день недели для напоминаний о выполнении привычки',
    )
    award = models.CharField(max_length=150, verbose_name='вознаграждение', **NULLABLE,
                             help_text='введите вознаграждение')
    time_perform = models.TimeField(verbose_name='время на выполнение',
                                    help_text='введите время на выполнение не более 120 секунд в формате ЧЧ:ММ:СС')
    is_public = models.BooleanField(default=False, verbose_name='признак публичной привычки',
                                    help_text='выберите, если хотите публиковать привычку')

    def clean(self):
        super().clean()

        # Проверка на время выполнения не более 120 секунд
        time_is_seconds = (self.time_perform.hour * 3600 + self.time_perform.minute * 60
                           + self.time_perform.second)
        if time_is_seconds > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд.')

        # Проверка на одновременный выбор связанной привычки и указания вознаграждения
        if self.linked_habit and self.award:
            raise ValidationError('Нельзя выбирать связанную привычку и указывать вознаграждение одновременно.')

        # Ограничение выбора связанной привычки только привычками с признаком приятной привычки
        if self.linked_habit and not self.linked_habit.pleasant_habit:
            raise ValidationError('Связанная привычка должна быть с признаком приятной привычки.')

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.pleasant_habit and (self.award or self.linked_habit):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')

        # Проверка на выбор как минимум одного дня недели
        if not self.reminder_frequency_days:
            raise ValidationError('Вы должны выбрать хотя бы один день недели для напоминания.')

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

    def __str__(self):
        return self.action
