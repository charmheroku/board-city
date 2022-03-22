from django.core.management.base import BaseCommand

from main.models import Seller

from django_seed import Seed


class Command(BaseCommand):

    help = "Эта команда создаст Продавца"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num", default=2, type=int, help="Сколько селлеров создать"
        )

    def handle(self, *args, **options):
        number = options.get("num")
        seeder = Seed.seeder()

        seeder.add_entity(
            Seller,
            number,
            {
                "kod_inn": "000000000000",
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} seller created!"))
