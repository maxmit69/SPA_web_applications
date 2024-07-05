from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'owner', 'place', 'time_start_habits', 'time_perform', 'is_public')
