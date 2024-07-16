from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class Command(BaseCommand):
    help = 'Для создания суперпользователя в базе данных django введите: python manage.py create_superuser'

    def handle(self, *args, **options):
        User = get_user_model()

        try:

            if not User.objects.filter(email='admin@localhost.com').exists():
                User.objects.create_superuser(
                    email='admin@localhost.com',
                    password='admin',
                    first_name='admin',
                    last_name='admin',
                )

                self.stdout.write(self.style.SUCCESS('Суперпользователь создан'))
            else:
                self.stdout.write(self.style.SUCCESS('Суперпользователь уже существует'))

        except ValidationError as e:
            raise CommandError(_('Ошибка при создании суперпользователя: %s') % '; '.join(e.messages))
