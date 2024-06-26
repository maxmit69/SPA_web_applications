from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

NULLABLE = {'null': True, 'blank': True}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Почта обязательна для заполнения')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):
    username = None

    email = models.EmailField(max_length=100, unique=True, verbose_name='почта', help_text='введите почту')
    tg_id = models.BigIntegerField(verbose_name='ID', unique=True, help_text='введите ID Telegram', **NULLABLE)
    phone = models.CharField(max_length=150, verbose_name='телефон', help_text='введите телефон', **NULLABLE)
    city = models.CharField(max_length=150, verbose_name='город', help_text='введите город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars/%Y/%m/%d', verbose_name='аватар', help_text='загрузите аватар',
                               **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
