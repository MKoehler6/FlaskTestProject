from flask import request, jsonify
from RestPlusAPI.api.myAPI import api
from flask_restplus import Resource
from RestPlusAPI.api.shop.api_definition import page_with_products, product
from RestPlusAPI.api.shop.parsers import pagination_parser as pagination
from RestPlusAPI.database.dtos import Product
from RestPlusAPI.api.shop.domain_logic import create_product

from RestPlusAPI.database import db as database

namespace = api.namespace('shop/products', description='Operations on my shop items')
productName = ''


@namespace.route('/')    # = /api/shop/products/
class Offer(Resource):

    @api.expect(pagination)
    @api.marshal_with(page_with_products)
    def get(self):
        args = pagination.parse_args(request)
        page = args.get('page', 1)
        items_per_page = args.get('items_per_page', 10)
        print(page , "  " , items_per_page)
        products = Product.query.paginate(page, items_per_page, error_out=False)
        return products

    @api.expect(product)
    def post(self):
        print(request.json)
        create_product(request.json)
        return None, 200


@namespace.route('/item/<int:id>')  # localhost:5000/api/shop/products/item/2
@namespace.route('/item/<int:year>/<int:month>/')
@api.response(404, 'There is no product with this ID yet')
class ProductItem(Resource):
    def get(self, id):
        product = Product.query.filter(Product.id == id).one()
        return jsonify(name=product.name, id=product.id)
