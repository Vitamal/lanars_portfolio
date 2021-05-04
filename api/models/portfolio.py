from . import BaseModel
from django.db import models


class Portfolio(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['created_datetime']

    def __str__(self):
        return self.name
