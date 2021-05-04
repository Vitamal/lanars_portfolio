from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from api.models import Image
from api.permissions import IsOwnerOrReadOnly
from api.serializers import ImageSerializer
from api.serializers.image import ImageListSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('created_datetime')
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'portfolio__name']

    def get_serializer_class(self):
        if self.action == 'list':
            return ImageListSerializer
        return ImageSerializer
