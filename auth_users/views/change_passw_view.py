from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from api.permissions import IsOwner
from auth_users.serializers import ChangePasswordSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = ChangePasswordSerializer
