from rest_framework import serializers
from api.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'image']


class CommentListSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(
        source='created_by.username')  # source argument controls which attribute is used to populate a field

    class Meta:
        model = Comment
        fields = ['id', 'name', 'comment', 'image', 'created_datetime', 'created_by']
        read_only_fields = ['created_datetime', 'created_by']
