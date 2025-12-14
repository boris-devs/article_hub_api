from django.db import models
from django_mongodb_backend.fields import ArrayField, ObjectIdField, ObjectIdAutoField


class Articles(models.Model):
    _id = ObjectIdAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = ArrayField(models.CharField(max_length=20))
    created_at = models.DateTimeField(auto_now_add=True)
    author = ObjectIdField(blank=False, null=False)
    analysis = models.JSONField(blank=True,null=True)