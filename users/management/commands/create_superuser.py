from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Для создания суперпользователя в базе данных django введите: python manage.py create_superuser'

    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(email='admin@localhost').exists():
            User.objects.create_superuser(
                email='admin@localhost',
                password='admin',
                first_name='Admin',
                last_name='Admin',
            )

            self.stdout.write(self.style.SUCCESS('Суперпользователь создан'))
        else:
            self.stdout.write(self.style.SUCCESS('Суперпользователь уже существует'))
