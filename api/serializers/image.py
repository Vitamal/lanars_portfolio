import os

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from api.models import Image
from api.serializers.create_update_premixin import CreateUpdatePreMixin

MAX_FILE_SIZE = 4 * 1024 * 1024


class ImageSerializer(CreateUpdatePreMixin, serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    created_by = serializers.ReadOnlyField(
        source='created_by.username')  # source argument controls which attribute is used to populate a field
    name = serializers.CharField(max_length=100, validators=[
        UniqueValidator(queryset=Image.objects.all())])  # Image name must be unique

    class Meta:
        model = Image
        fields = ['id', 'name', 'description', 'portfolio', 'comments', 'created_by', 'created_datetime', 'upload']
        read_only_fields = ['created_by', 'created_datetime']

    def validate_upload(self, image):
        # 4MB
        if image.size > MAX_FILE_SIZE:
            raise ValidationError("File size too big!")

        # if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        #     raise ValidationError("Invalid file type.")

class ImageListSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source='created_by.username')

    class Meta:
        model = Image
        fields = ['id', 'name', 'description', 'portfolio', 'created_datetime', 'created_by']
        read_only_fields = ['created_datetime', 'created_by']
