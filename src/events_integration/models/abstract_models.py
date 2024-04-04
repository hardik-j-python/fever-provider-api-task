from django.db import models


class TimeAuditedModel(models.Model):
    creation_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    modification_datetime = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        abstract = True
