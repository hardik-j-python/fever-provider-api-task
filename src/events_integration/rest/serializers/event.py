from django.db.models import Max, Min
from rest_framework import serializers

from events_integration.models import Event


class EventSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    start_time = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    max_price = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.uuid

    def get_start_date(self, obj):
        return obj.event_start_datetime.date().isoformat()

    def get_start_time(self, obj):
        return obj.event_start_datetime.time().isoformat()

    def get_end_date(self, obj):
        return obj.event_end_datetime.date().isoformat()

    def get_end_time(self, obj):
        return obj.event_end_datetime.time().isoformat()

    def get_min_price(self, obj):
        return obj.zones.aggregate(min_price=Min('price'))['min_price']

    def get_max_price(self, obj):
        return obj.zones.aggregate(max_price=Max('price'))['max_price']

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'start_date', 'start_time',
            'end_date', 'end_time', 'min_price', 'max_price'
        ]
