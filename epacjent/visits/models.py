import uuid
from django.db import models
from django.contrib.auth.models import User

class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    visit_date = models.DateField(null=True, blank=True)
    visit_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name
