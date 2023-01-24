"""
Command for clearing and creating fake data in the database.
Intended for use in development.
"""

from typing import Any, Callable
from django.core.management.base import BaseCommand, CommandError, CommandParser
from namu.models import Namuseta, User, Product, Transaction, Deposit, Restock, Feedback
from django.conf import settings
import random
from faker import Faker

# Autocomplete for this doesn't work for me (mUusitalo) in VSCode as of 23.1.2023
fake = Faker(locale=["fi_FI", "en_US"])

# Appending this to all fake data as a backup just in case this command gets accidentally used in production
DEV_POSTFIX = "@DEV"

class Command(BaseCommand):
    help = "Adds some data to the database. Only use in development!"
    
    def add_arguments(self, parser: CommandParser):
        parser.add_argument("-n", "--namuseta", nargs="?", required=False, type=int, default=5)
        parser.add_argument("-u", "--user", nargs="?", required=False, type=int, default=100)
        parser.add_argument("-p", "--product", nargs="?", required=False, type=int, default=20)
        parser.add_argument("-t", "--transaction", nargs="?", required=False, type=int, default=1000)
        parser.add_argument("-d", "--deposit", nargs="?", required=False, type=int, default=100)
        parser.add_argument("-r", "--restock", nargs="?", required=False, type=int, default=50)
        parser.add_argument("-f", "--feedback", nargs="?", required=False, type=int, default=50)

    def _create_rows(self, model, generate_data: Callable[[], dict[str, Any]], count: int):
        objects = (model(**generate_data()) for _ in range(count))
        model.objects.bulk_create(objects)

    def _create_namuseta_rows(self, count: int):
        def generate_data():
            first_name = fake.first_name()
            last_name = fake.last_name()
            name = f"{first_name} {last_name}" + DEV_POSTFIX
            mobilepay = fake.unique.phone_number() + DEV_POSTFIX
            contact = f"{first_name}.{last_name}@{fake.domain_name()}" + DEV_POSTFIX
            return {"name": name, "mobilepay": mobilepay, "contact": contact,}
        self._create_rows(Namuseta, generate_data, count)

    def _create_user_rows(self, count: int):
        def generate_data():
            name = fake.name() + DEV_POSTFIX
            is_active = fake.boolean(chance_of_getting_true=50)
            return {"name": name, "is_active": is_active,}
        self._create_rows(User, generate_data, count)

    def _create_product_rows(self, count: int):
        def generate_data():
            name = fake.word() + DEV_POSTFIX
            category = random.choice([category[0] for category in Product.CATEGORY_OPTIONS])
            price = random.uniform(0.1, 5.0)
            cost = price + random.uniform(-0.1, 0.1)
            picture = fake.image_url()
            is_active = fake.boolean(chance_of_getting_true=50)
            return {
                "name": name,
                "category": category,
                "price": price,
                "cost": cost,
                "picture": picture,
                "is_active": is_active,
            }
        return self._create_rows(Product, generate_data, count)

    def _create_transaction_rows(self, count: int):
        
        products = list(Product.objects.all())
        users = list(User.objects.all())

        def generate_data():
            timestamp = fake.date_between()
            user = random.choice(users)
            product = random.choice(products)
            price = product.price
            cost = product.cost
            return {
                "timestamp": timestamp,
                "user": user,
                "product": product,
                "price": price,
                "cost": cost,
            }

        self._create_rows(Transaction, generate_data, count)

    def _create_deposit_rows(self, count: int):
        users = list(User.objects.all())

        def generate_data():
            timestamp = fake.date_between()
            user = random.choice(users)
            amount = random.uniform(0.01, 100)
            payment_method = "m"
            return {
                "timestamp": timestamp,
                "user": user,
                "amount": amount,
                "payment_method": payment_method,
            }

        self._create_rows(Deposit, generate_data, count)

            
    def _create_restock_rows(self, count: int):
        products = list(Product.objects.all())
        
        def generate_data():
            timestamp = fake.date_between()
            product = random.choice(products)
            quantity = random.randrange(1, 500)
            type = Restock.RESTOCK_TYPES[0][0] if random.uniform(0, 1) > 0.1 else Restock.RESTOCK_TYPES[1][0]
            return {
                "timestamp": timestamp,
                "product": product,
                "quantity": quantity,
                "type": type,
            }

        self._create_rows(Restock, generate_data, count)


    def _create_feedback_rows(self, count: int):
        def generate_data():
            timestamp = fake.date_between()
            title = fake.catch_phrase() + DEV_POSTFIX
            message = fake.paragraph(nb_sentences=3) + DEV_POSTFIX
            return {
                "timestamp": timestamp,
                "title": title,
                "message": message,
            }

        self._create_rows(Feedback, generate_data, count)

    def _create_fake_rows(self, **options):
        self._create_namuseta_rows(options["namuseta"])
        self._create_user_rows(options["user"])
        self._create_deposit_rows(options["deposit"])
        self._create_product_rows(options["product"])
        self._create_restock_rows(options["restock"])
        self._create_transaction_rows(options["transaction"])
        self._create_feedback_rows(options["feedback"])
        
    def handle(self, **options):
        confirmation_ok = input("""This command will write fake rows to the database. This is IRREVERSIBLE. Type "eiookettu" to proceed, leave blank to cancel: """) == "eiookettu"
        if not confirmation_ok:
            raise CommandError("Canceled")

        print("Creating fake data")
        self._create_fake_rows(**options)
        print("Done")



