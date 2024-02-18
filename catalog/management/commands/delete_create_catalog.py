import json
from catalog.models import Product, Category
from django.core.management import BaseCommand


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        with open('fixtures/catalog_categories.json', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def json_read_products():
        with open('fixtures/catalog_products.json', encoding='utf-8') as f:
            return json.load(f)

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category_for_create = []
        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    pk=category['pk'],
                    name=category['fields']['name'],
                    description=category['fields']['description']
                )
            )

        Category.objects.bulk_create(category_for_create)

        product_for_create = []
        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    pk=product['pk'],
                    name=product['fields']['name'],
                    description=product['fields']['description'],
                    image_preview=product['fields']['image_preview'],
                    category=Category.objects.get(pk=product['fields']['category']),
                    price=product['fields']['price'],
                )
            )

        Product.objects.bulk_create(product_for_create)




