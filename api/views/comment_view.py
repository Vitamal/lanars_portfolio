from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import serializers
from api.models import Comment
from api.serializers import CommentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, image_pk):
    """
    Create comment for the image.
    """

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
