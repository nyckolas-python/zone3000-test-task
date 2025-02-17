import uuid

from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models


class RedirectRule(models.Model):
    """
    Model for storing redirect rules.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    redirect_url = models.URLField(max_length=200, validators=[URLValidator()])
    is_private = models.BooleanField(default=False)
    redirect_identifier = models.CharField(max_length=8, unique=True, editable=False)

    def __str__(self):
        return f"{self.redirect_identifier} -> {self.redirect_url}"

    def save(self, *args, **kwargs):
        if not self.redirect_identifier:
            self.redirect_identifier = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
