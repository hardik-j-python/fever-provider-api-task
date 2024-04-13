import uuid

from django.db import models

from .abstract_models import TimeAuditedModel


class BaseEvent(TimeAuditedModel):
    id = models.AutoField(primary_key=True)

    base_event_id = models.IntegerField(null=False, blank=False,)
    organizer_company_id = models.IntegerField(null=True, blank=False)

    title = models.CharField(null=False, blank=False, max_length=128, editable=True)
    sell_mode = models.CharField(null=False, blank=False, max_length=32, editable=False)

    class Meta:
        abstract = True


class Event(BaseEvent):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    event_start_datetime = models.DateTimeField(null=False, blank=False, db_index=True)
    event_end_datetime = models.DateTimeField(null=False, blank=False, db_index=True)
    sell_from = models.DateTimeField(null=False, blank=False)
    sell_to = models.DateTimeField(null=False, blank=False)

    sold_out = models.BooleanField(null=False, blank=False)

