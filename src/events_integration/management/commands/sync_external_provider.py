from django.core.management import BaseCommand

from events_integration.rest.utils.sync_external_events import SyncExternalEvents


class Command(BaseCommand):
    help = "Syncs events from external provider"

    def handle(self, *args, **options):
        url = "https://provider.code-challenge.feverup.com/api/events"
        SyncExternalEvents(api_path=url).start()
