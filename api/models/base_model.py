from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    """
        Abstract model to provide basic fields
        common for all HH models.

        """

    #: Automatically set the field to now when the object is first created.
    created_datetime = models.DateTimeField(auto_now_add=True)

    #: Automatically set the field to now every time the object is saved.
    changed_datetime = models.DateTimeField(auto_now=True)

    #: Who created the instance
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='+')

    #: Who was the last user to modify/update the instance
    changed_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        abstract = True
