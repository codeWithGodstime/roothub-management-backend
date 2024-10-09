from django.db import models

from .util_functions import generate_uuid



class BaseModelMixin(models.Model):

    id = models.CharField(max_length=300, unique=True, db_index=True, primary_key=True, default=generate_uuid)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True