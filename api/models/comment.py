from . import BaseModel, Image
from django.db import models


class Comment(BaseModel):
    comment = models.TextField(max_length=100)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.comment
