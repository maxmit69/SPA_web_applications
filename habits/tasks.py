from celery import shared_task
import requests
from .models import Habit
from django.utils import timezone
from django.conf import settings


@shared_task
def send_habit_reminders():
    """Отправляет напоминания о выполнении привычки"""
    now = timezone.localtime()
    current_time = now.strftime('%H:%M:%S')  # текущее время в формате часы:минуты:секунды
    current_day = now.strftime('%a').lower()[:3]    # текущий день недели в нижнем регистре (пример: 'mon')

    habits = Habit.objects.filter(time_start_habits=current_time, reminder_frequency_days=current_day)

    for habit in habits:
        if habit.owner.tg_id:
            send_telegram_message.delay(chat_id=habit.owner.tg_id,
                                        text=f"Напоминание: {habit.action} в {habit.time_start_habits}")
        else:
            raise Exception("У пользователя нет Telegram ID")


@shared_task
def send_telegram_message(chat_id, text):
    """Отправляет сообщение в Telegram"""
    params = {
        'chat_id': chat_id,
        'text': text
    }
    requests.get(f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage', params=params)
