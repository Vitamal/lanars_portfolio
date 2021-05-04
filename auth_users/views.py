from django.contrib.auth import get_user_model
from rest_framework import generics

from rest_framework.permissions import AllowAny

from api.permissions import IsOwner
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class UserView(generics.RetrieveUpdateDestroyAPIView):
    model = get_user_model()
    permission_classes = [IsOwner]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj
