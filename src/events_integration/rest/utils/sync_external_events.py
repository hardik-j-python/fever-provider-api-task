import datetime
import logging
from typing import List

import requests
import xmltodict
from rest_framework import status

from events_integration.models import Event, Zone

logger = logging.getLogger("sync_external_events")


class SyncExternalEvents:
    def __init__(self, api_path: str):
        self.api_path = api_path
        self.request = None

    def is_request_status_ok(self):
        return self.request.status_code in (status.HTTP_200_OK,)

    @staticmethod
    def _datetime_string_parser(datetime_str: str, datetime_parser_mask="%Y-%m-%dT%H:%M:%S"):
        return datetime.datetime.strptime(datetime_str, datetime_parser_mask)

    @staticmethod
    def _add_zone(zone, event_id, zones_to_update_by_id):
        zone_data = dict()
        zone_data_id = int(zone["@zone_id"])
        zone_data["id"] = zone_data_id
        zone_data["event_id"] = event_id
        zone_data["capacity"] = int(zone["@capacity"])
        zone_data["price"] = float(zone["@price"])
        zone_data["name"] = zone["@name"]
        zone_data["numbered"] = zone["@numbered"] == "true"
        zones_to_update_by_id[zone_data_id] = Zone(**zone_data)

    def _zones_parser(self, event_zones, event_id, zones_to_update_by_id):
        if isinstance(event_zones, list):
            for zone in event_zones:
                self._add_zone(zone, event_id, zones_to_update_by_id)
        else:
            self._add_zone(event_zones, event_id, zones_to_update_by_id)

    def _event_parser(self, base_event, event, events_to_update_by_id):
        try:
            event_id = int(event["@event_id"])
            event_data = {
                "id": event_id,
                "base_event_id": int(base_event["@base_event_id"]),
                "organizer_company_id": base_event.get("@organizer_company_id", None),
                "title": base_event["@title"],
                "sell_mode": base_event["@sell_mode"],
                "event_datetime": self._datetime_string_parser(event["@event_start_date"]),
                "sell_from": self._datetime_string_parser(event["@sell_from"]),
                "sell_to": self._datetime_string_parser(event["@sell_to"]),
                "sold_out": event["@sold_out"] == "true",
            }

            events_to_update_by_id[event_id] = Event(**event_data)
        except Exception as exc:
            # Invalid data
            pass

    def _get_events_and_zones_to_update(self, base_events: List):
        events_to_update_by_id = dict()
        zones_to_update_by_id = dict()

        for base_event in base_events:
            sell_mode = base_event["@sell_mode"]
            if sell_mode == "online":
                event = base_event["event"]
                event_zones = event["zone"]
                event_id = int(event["@event_id"])

                self._zones_parser(event_zones, event_id, zones_to_update_by_id)
                self._event_parser(base_event, event, events_to_update_by_id)

        return events_to_update_by_id, zones_to_update_by_id

    @staticmethod
    def _bulk_update_or_create(model, ids_in_bbdd, obj, fields):
        obj_to_create = list()
        objs_to_update = list()
        for key, value in obj.items():
            if key in ids_in_bbdd:
                objs_to_update.append(value)
            else:
                obj_to_create.append(value)

        model.objects.bulk_create(obj_to_create, ignore_conflicts=True)
        model.objects.bulk_update(objs_to_update, fields=fields)

    def start(self):
        try:
            self.request = requests.get(self.api_path)
        except:
            # Connection error
            return

        xml_dict = xmltodict.parse(self.request.content)
        base_events = xml_dict["eventList"]["output"]["base_event"]
        events_to_update_by_id, zones_to_update_by_id = self._get_events_and_zones_to_update(base_events)

        event_ids_in_bbdd = Event.objects.filter(id__in=events_to_update_by_id.keys()).values_list("id", flat=True)
        self._bulk_update_or_create(
            Event, event_ids_in_bbdd, events_to_update_by_id, ["event_datetime", "sell_from", "sell_to", "sell_mode"]
        )

        zone_ids_in_bbdd = Zone.objects.filter(id__in=zones_to_update_by_id.keys()).values_list("id", flat=True)
        self._bulk_update_or_create(
            Zone, zone_ids_in_bbdd, zones_to_update_by_id, ["capacity", "price", "numbered", "event_id"]
        )
