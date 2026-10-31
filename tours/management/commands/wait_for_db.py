import time

from django.core.management.base import BaseCommand, CommandError
from django.db import OperationalError, connections


class Command(BaseCommand):
    help = "Wait for an authenticated PostgreSQL connection, with bounded retries."

    def add_arguments(self, parser):
        parser.add_argument("--attempts", type=int, default=30)
        parser.add_argument("--delay", type=float, default=1)

    def handle(self, *args, **options):
        database = connections["default"]
        for attempt in range(options["attempts"]):
            try:
                with database.cursor() as cursor:
                    cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS("PostgreSQL is ready."))
                return
            except OperationalError:
                database.close()
                self.stdout.write(f"Waiting for PostgreSQL ({attempt + 1}/{options['attempts']})...")
                if attempt + 1 < options["attempts"]:
                    time.sleep(options["delay"])
        raise CommandError("PostgreSQL did not become ready. Check database settings and logs.")
