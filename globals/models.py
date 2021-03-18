import uuid
import pytz
from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class Timestamp(models.Model):
    """Model containg created and last modified time"""
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="Primary key")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    last_modified_at = models.DateTimeField(default=timezone.now, verbose_name="Last modified at")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.last_updated_at = datetime.now(pytz.utc)


