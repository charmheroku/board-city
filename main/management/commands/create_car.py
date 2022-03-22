import random
from django.core.management.base import BaseCommand

from main.models import CarAdvert, Seller, Category

from django_seed import Seed
from faker import Faker
from faker_vehicle import VehicleProvider


class Command(BaseCommand):

    help = "Эта команда создаст объявления Авто"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num", default=2, type=int, help="Сколько объявлений создать"
        )

    def handle(self, *args, **options):
        number = options.get("num")
        seeder = Seed.seeder()
        fake = Faker()
        fake.add_provider(VehicleProvider)
        category = Category.objects.get(pk=1)
        sellers = Seller.objects.all()

        seeder.add_entity(
            CarAdvert,
            number,
            {
                "category": category,
                "seller": lambda x: random.choice(sellers),
                "color": lambda x: seeder.faker.safe_color_name(),
                "brand": lambda x: fake.vehicle_make(),
                "model": lambda x: fake.vehicle_make_model(),
                "year": lambda x: fake.vehicle_year(),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} advert created!"))
