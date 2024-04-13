import datetime
import logging

from rest_framework import viewsets, mixins, status
from rest_framework.exceptions import ParseError

from events_integration.models import Event
from events_integration.rest.serializers.event import EventSerializer

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

        return self.model.objects.filter(event_start_datetime__gte=starts_at, event_end_datetime__lte=ends_at_datetime_obj)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('starts_at', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
            openapi.Parameter('ends_at', openapi.IN_QUERY, type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
        ],
        responses={200: openapi.Response(
            description="List of plans",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'events': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_STRING),
                                        'title': openapi.Schema(type=openapi.TYPE_STRING),
                                        'start_date': openapi.Schema(type=openapi.TYPE_STRING),
                                        'start_time': openapi.Schema(type=openapi.TYPE_STRING),
                                        'end_date': openapi.Schema(type=openapi.TYPE_STRING),
                                        'end_time': openapi.Schema(type=openapi.TYPE_STRING),
                                        'min_price': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'max_price': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    }
                                )
                            )
                        }
                    ),
                    'error': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                }
            ),
            examples={
                "application/json": {
                    "data": {
                        "events": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                "title": "string",
                                "start_date": "2024-04-13",
                                "start_time": "22:38:19",
                                "end_date": "2024-04-13",
                                "end_time": "14:45:15",
                                "min_price": 0,
                                "max_price": 0
                            }
                        ]
                    },
                    "error": None
                }
            }
        ), 400: openapi.Response(
                description="The request was not correctly formed (missing required parameters, wrong types...)",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_STRING),
                                'message': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'data': openapi.Schema(type=openapi.TYPE_STRING, format="null")
                    }
                ),
                examples={
                    "application/json": {
                        "error": {
                            "code": "string",
                            "message": "string"
                        },
                        "data": None  # Null data
                    }
                }
            ),
            500: openapi.Response(
                description="Generic error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_STRING),
                                'message': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'data': openapi.Schema(type=openapi.TYPE_STRING, format="null")
                    }
                ),
                examples={
                    "application/json": {
                        "error": {
                            "code": "string",
                            "message": "string"
                        },
                        "data": None  # Null data
                    }
                }
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response_data = {"data": {"events": response.data}, "error": None}
        response.data = response_data

        return response
