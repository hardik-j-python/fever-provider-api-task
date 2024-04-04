from django.db import models

from .abstract_models import TimeAuditedModel
from .event import Event


class Zone(TimeAuditedModel):
    event = models.ForeignKey(Event, null=False, on_delete=models.CASCADE, related_name='zones')

    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=128, editable=True)

    capacity = models.IntegerField(blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    numbered = models.BooleanField(default=True)
