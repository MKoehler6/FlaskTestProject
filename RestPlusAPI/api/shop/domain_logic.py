from RestPlusAPI.database import db
from RestPlusAPI.database.dtos import Product


def create_product(data):
    name = data.get('name')
    product = Product(name)
    db.add(product)


def read_product(data):
    id = data.get('id')
    product = db.find(id)
    return product


def update_product(data):
    id = data.get('id')
    name = data.get('name')
    db.update(id, name)


def delete_product(data):
    id = data.get('id')
    db.delete(id)

