import datetime
import logging

from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ParseError

from events_integration.models import Event
from events_integration.rest.serializers.event import EventSerializer

logger = logging.getLogger("sync_external_events")


class EventsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    model = Event
    serializer_class = EventSerializer

    @staticmethod
    def _datetime_string_parser(datetime_str: str, datetime_parser_mask="%Y-%m-%dT%H:%M:%SZ"):
        errored = False
        date_time_obj = None
        try:
            date_time_obj = datetime.datetime.strptime(datetime_str, datetime_parser_mask)
        except:
            errored = True

        return errored, date_time_obj

    def get_queryset(self):
        starts_at = self.request.query_params.get("starts_at", None)
        errored, starts_at_datetime_obj = self._datetime_string_parser(starts_at)
        if errored:
            error_message = f"Query param: 'starts_at' not provided or malformed."
            detail = {"error": {"message": error_message, "code": status.HTTP_400_BAD_REQUEST}, "data": None}
            raise ParseError(detail, code=status.HTTP_400_BAD_REQUEST)

        ends_at = self.request.query_params.get("ends_at", None)
        errored, ends_at_datetime_obj = self._datetime_string_parser(ends_at)
        if errored:
            error_message = f"Query param: 'ends_at' not provided or malformed."
            detail = {"error": {"message": error_message, "code": status.HTTP_400_BAD_REQUEST}, "data": None}
            raise ParseError(detail, code=status.HTTP_400_BAD_REQUEST)

        return self.model.objects.filter(event_datetime__gte=starts_at, event_datetime__lte=ends_at_datetime_obj)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = {"data": {"events": response.data}}
        response.data = response_data

        return response
