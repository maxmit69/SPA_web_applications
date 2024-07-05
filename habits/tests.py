from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from habits.models import Habit
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


class HabitCRUTestCase(APITestCase):

    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create_user(email='testuser@localhost.com', password='testpassword')
        self.user2 = User.objects.create_user(email='testuser2@localhost.com', password='testpassword2')

        # Создание привычки
        self.habit = Habit.objects.create(place='Test place', time_start_habits='09:00:00', action='Test action',
                                          pleasant_habit=False, reminder_frequency_days='mon', time_perform='00:01:00',
                                          is_public=False, linked_habit=None, award=None, owner=self.user)

        # Создание данных для обновления привычки
        self.new_habit_data = {
            'place': 'New habit',
            'time_start_habits': '08:00:00',
            'action': 'New action',
            'time_perform': '00:01:00',
            'reminder_frequency_days': 'wed',
            'owner': self.user.id
        }
        self.update_habit_data = {
            'place': 'Updated habit',
            'time_start_habits': '09:00:00',
            'action': 'Updated action',
            'time_perform': '00:01:00',
            'reminder_frequency_days': 'thu',
            'owner': self.user.id
        }

        # URL адреса
        self.habit_list_url = reverse('habits:habits-list')
        self.habit_public_list_url = reverse('habits:public-habits')
        self.habit_create_url = reverse('habits:create-habit')
        self.habit_update_url = reverse('habits:update-habit', args=[self.habit.id])
        self.habit_delete_url = reverse('habits:delete-habit', args=[self.habit.id])

    def test_list_public_habits_as_anonymous(self):
        """ Список привычек неавторизованным пользователем """
        response = self.client.get(self.habit_public_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_habits_as_anonymous(self):
        """ Список привычек неавторизованным пользователем """
        response = self.client.get(self.habit_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_habits_as_user(self):
        """ Список привычек авторизованным пользователем """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.habit_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['place'], 'Test place')

    def test_update_habit_as_user(self):
        """ Обновление привычки авторизованным пользователем """
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.habit_update_url, self.update_habit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(Habit.objects.get(pk=self.habit.id).place)
        self.assertEqual(Habit.objects.get(pk=self.habit.id).place, 'Updated habit')

    def test_create_habit_as_user(self):
        """ Создание привычки авторизованным пользователем """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.habit_create_url, self.new_habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(Habit.objects.get(pk=2).place, 'New habit')

    def test_create_habit_as_user_not_authorized(self):
        """ Создание привычки неавторизованным пользователем """
        response = self.client.post(self.habit_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_habits_as_user_not_authorized(self):
        """ Список привычек неавторизованным пользователем """
        response = self.client.get(self.habit_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_habit_as_user_not_owner(self):
        """ Обновление привычки другим авторизованным пользователем """
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(self.habit_update_url, self.update_habit_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_habit_as_user(self):
        """ Удаление привычки авторизованным пользователем """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.habit_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_delete_habit_as_user_not_owner(self):
        """ Удаление привычки другим авторизованным пользователем """
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.habit_delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
