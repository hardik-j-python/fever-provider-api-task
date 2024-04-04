from rest_framework import serializers

from events_integration.models import Zone


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        # fields = '__all__'
        exclude = [
            'creation_datetime', 'modification_datetime'
        ]
