from django.urls import path
from habits import views

from habits.apps import HabitsConfig

app_name = HabitsConfig.name

urlpatterns = [
    path('habit/', views.HabitListApiView.as_view(), name='habits-list'),
    path('public-habits/', views.PublicHabitListApiView.as_view(), name='public-habits'),
    path('create-habit/', views.HabitCreateApiView.as_view(), name='create-habit'),
    path('update-habit/<int:pk>/', views.HabitUpdateApiView.as_view(), name='update-habit'),
    path('delete-habit/<int:pk>/', views.HabitDestroyApiView.as_view(), name='delete-habit'),

]