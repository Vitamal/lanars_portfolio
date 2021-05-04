from . import BaseModel, Portfolio
from django.db import models


def portfolio_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<project.name>/<filename>
    return 'user_{0}/{1}/{2}'.format(instance.created_by.id, instance.portfolio.name, filename)


class Image(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='images')
    upload = models.ImageField(
        upload_to=portfolio_directory_path)  # https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.FileField.upload_to

    class Meta:
        ordering = ['created_datetime']
