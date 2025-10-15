import requests
from rest_framework.exceptions import NotFound

from core.models import Product
from core.utils.cache import cached_func

URL = "https://fakestoreapi.com"
FIELDS = ["id", "title", "price", "image"]

@cached_func()
def get_all_products() -> list[dict]:
    response = requests.get(f'{URL}/products')
    response.raise_for_status()
    products = response.json()

    filtered_products = [{field: product.get(field) for field in FIELDS} for product in products]

    return filtered_products

@cached_func()
def get_product(id: int) -> dict:
    response = requests.get(f'{URL}/products/{id}')
    if not response.content:
        raise NotFound('Product not found')
    response.raise_for_status()
    product = response.json()

    filtered_product = {field: product.get(field) for field in FIELDS}

    return filtered_product

def insert_product_in_database(id: int) -> Product:
    try:
        product = Product.objects.get(pk=id)
        return product
    except Product.DoesNotExist:
        data = get_product(id)
        product = Product.objects.create(
            id=data.get("id"),
            title=data.get("title"),
            price=data.get("price"),
            image=data.get("image"),
        )
        return product
