from flask_restplus import fields
from RestPlusAPI.api.myAPI import api
from flask_restplus import Resource

product = api.model('Product', {
    'id': fields.Integer(readOnly = True, description='The Identifier of the product'),
    'name': fields.String(required = True, description='Product Name'),
})

category = api.model('Product Category', {
    'id': fields.Integer(readOnly=True, description='The Identifier of the category'),
    'name': fields.String(required=True, description='Category name')
})

pagination = api.model('One page of products', {
    'page': fields.Integer(description='Current page'),
    'pages': fields.Integer(description='Total pages'),
    'items_per_page': fields.Integer(description='Items per Page'),
    'total_items': fields.Integer(description='Total amount of items')
})

page_with_products = api.inherit('Page with products', pagination, {
    'items': fields.List(fields.Nested(product))
})