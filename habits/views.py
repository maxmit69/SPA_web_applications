from rest_framework import generics, permissions
from habits.paginators import HabitPagination
from habits.serializers import HabitSerializer
from habits.models import Habit
from django.contrib.auth.models import AnonymousUser


class HabitListApiView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """ Получает список привычек пользователя """
        return Habit.objects.filter(owner=self.request.user).order_by('id')


class PublicHabitListApiView(generics.ListAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [permissions.AllowAny]


class HabitCreateApiView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """ Сохраняет привычку пользователя """
        serializer.save(owner=self.request.user)


class HabitUpdateApiView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Возвращает список привычек пользователя """
        if isinstance(self.request.user, AnonymousUser):
            return Habit.objects.none()
        return Habit.objects.filter(owner=self.request.user)


class HabitDestroyApiView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Возвращает список привычек пользователя """
        if isinstance(self.request.user, AnonymousUser):
            return Habit.objects.none()
        return Habit.objects.filter(owner=self.request.user)
