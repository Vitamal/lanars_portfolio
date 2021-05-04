from rest_framework import serializers
from api.models import Portfolio
from api.serializers.create_update_premixin import CreateUpdatePreMixin


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['name', 'description']


class PortfolioListSerializer(CreateUpdatePreMixin, serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source='created_by.username')

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'description', 'created_datetime', 'created_by']

    read_only_fields = ['created_datetime', 'created_by']
