from rest_framework import serializers
from api.models import Portfolio
from api.serializers import ImageSerializer
from api.serializers.create_update_premixin import CreateUpdatePreMixin


class PortfolioSerializer(CreateUpdatePreMixin, serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ['name', 'description', 'images']


class PortfolioListSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source='created_by.username')

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'description', 'created_datetime', 'created_by']

    read_only_fields = ['created_datetime', 'created_by']
