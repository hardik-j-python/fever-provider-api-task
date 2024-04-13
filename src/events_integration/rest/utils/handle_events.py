from abc import ABC, abstractmethod


class BaseSyncExternalEvents(ABC):
    """
    Abstract base class for synchronizing external events.
    """

    def __init__(self, api_path):
        """
        Initialize the BaseSyncExternalEvents.

        Args:
            api_path (str): The API path to retrieve external events data.
        """
        self.api_path = api_path
        self.request = None

    @abstractmethod
    def handle_request(self):
        """
        Abstract method to handle the HTTP request to fetch external events data.
        """

        pass

    @abstractmethod
    def parse_date(datetime_str, datetime_parser_mask):
        """
        Abstract static method to parse datetime strings.

        Args:
            datetime_str (str): The datetime string to parse.
            datetime_parser_mask (str): The format mask for parsing the datetime string.
        """

        pass

    @abstractmethod
    def parse_zone(self, event_zones, event_id, zone_data_dict):
        """
        Abstract method to parse event zones data.

        Args:
            event_zones: The zone data for an event.
            event_id: The ID of the event.
            zone_data_dict: A dictionary to store parsed zone data.
        """

        pass

    @abstractmethod
    def parse_event(self, base_event, event, event_data_dict):
        """
        Abstract method to parse event data.

        Args:
            base_event: The base event data.
            event: The event data.
            event_data_dict: A dictionary to store parsed event data.
        """

        pass

    @abstractmethod
    def get_events_and_zones_to_update(self, base_events):
        """
        Abstract method to extract events and zones data from the API response.

        Args:
            base_events: The list of base events data.
        """

        pass

    @abstractmethod
    def handle_bulk_update_or_create(model, records_ids_in_db, objects, fields):
        """
        Abstract static method to handle bulk update or create operations.

        Args:
            model: The model class for which bulk update or create is performed.
            records_ids_in_db: A list of IDs already existing in the database.
            objects: The objects to update or create.
            fields: The fields to update in case of existing records.
        """

        pass

    @abstractmethod
    def start(self):
        """
        Abstract method to start the synchronization process.
        """

        pass