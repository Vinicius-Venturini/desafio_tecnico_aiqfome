from core.models import Client, Product, ClientProduct
from core.services.product import insert_product_in_database

def update_client(client: Client, data: dict) -> Client:
    allowed_fields = ['name']
    password = None

    if 'id' in data:
        raise ValueError('You can\'t modify the "id" field')
    
    if 'email' in data:
        raise ValueError('You can\'t modify the "email" field')
    
    if 'password' in data:
        password = data.pop('password')

    for field, value in data.items():
        if field in allowed_fields:
            setattr(client, field, value)

    if password:
        client.set_password(password)

    client.save()

    return client

def favorite_product(client: Client, product_id: int, review: str = "", rating: int = 3) -> ClientProduct:
    product = insert_product_in_database(product_id)
    
    client_product = ClientProduct.objects.create(
        client=client,
        product=product,
        rating=rating,
        review=review
    )

    return client_product
