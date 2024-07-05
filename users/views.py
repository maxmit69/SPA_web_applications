from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializers import UserSerializer


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """ Сохранение пользователя с хэшем пароля """
        user = serializer.save(is_active=True)
        user.set_password(self.request.data['password'])
        user.save()
