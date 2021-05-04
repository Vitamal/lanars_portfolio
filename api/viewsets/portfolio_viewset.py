from rest_framework import viewsets, permissions

from api.models import Portfolio
from api.permissions import IsOwnerOrReadOnly
from api.serializers import PortfolioSerializer, PortfolioListSerializer


class PortfolioViewSet(viewsets.ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Portfolio.objects.filter(created_by=self.request.user).order_by('created_datetime')

    def get_serializer_class(self):
        if self.action == 'list':
            return PortfolioListSerializer
        return PortfolioSerializer
