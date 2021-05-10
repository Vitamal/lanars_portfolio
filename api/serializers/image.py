from rest_framework import serializers
from api.models import Image
from api.serializers.create_update_premixin import CreateUpdatePreMixin


class ImageSerializer(CreateUpdatePreMixin, serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(
        source='created_by.username')  # source argument controls which attribute is used to populate a field

    class Meta:
        model = Image
        fields = ['id', 'name', 'description', 'portfolio', 'comments', 'created_by', 'created_datetime', 'upload']
        read_only_fields = ['created_by', 'created_datetime']


class ImageListSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source='created_by.username')

    class Meta:
        model = Image
        fields = ['id', 'name', 'description', 'portfolio', 'created_datetime', 'created_by']
        read_only_fields = ['created_datetime', 'created_by']
