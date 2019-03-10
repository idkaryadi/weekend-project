import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from blueprints import db
from blueprints.auth import Clients
from blueprints.client import Products, Product_Types
from blueprints.user import Transaction_Details
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_client = Blueprint('client', __name__)
api = Api(bp_client)

# Bagian Resource untuk Clients
class ClientResource(Resource):

    @jwt_required
    def get(self):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}
        client_id = jwtClaims['id']
        qry = Clients.query.get(client_id)
        if qry is None:
            return {"status": "Your Account is deleted by your self"}, 404, {'Content-Text':'application/json'}
        # return jwtClaims, 200, {'Content-Text':'application/json'}
        return marshal(qry, Clients.respond_field), 200, {'Content-Text':'application/json'}

    @jwt_required
    def put(self):
        jwtClaims = get_jwt_claims()

        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}

        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json')
        parser.add_argument('password', location = 'json')
        args = parser.parse_args()

        client_id = jwtClaims["id"]
        qry = Clients.query.get(client_id)
        if qry is None:
            return {"status": "Your Account is deleted by your self"}, 404, {'Content-Text':'application/json'}

        if args['username'] is not None:
            qry.username = args['username']
        if args['password'] is not None:
            qry.password = args["password"]
        
        db.session.commit()
        return {"status": "Success Updated User Data"}, 200, {'Content-Text':'application/json'}
    
    @jwt_required
    def delete(self):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}
        
        client_id = jwtClaims["id"]
        qry = Clients.query.get(client_id)

        if qry is None:
            return {"status": "Your Account is deleted by your self"}, 404, {'Content-Text':'application/json'}

        db.session.delete(qry)
        db.session.commit()
        return {"status": "Success deleted"}, 200, {'Content-Text':'application/json'}

api.add_resource(ClientResource, '/client')

class ClientProductsResource(Resource):

    @jwt_required
    def get(self, id = None):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}
        
        client_id = jwtClaims['id']
        Product = Products.query.filter_by(client_id = client_id)

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location = 'args', default = 1)
        parser.add_argument('rp', type=int, location = 'args', default = 5)
        parser.add_argument('q', location = 'args', default = "")

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']
        
        output = dict()

        if id is None:
            qry = Product
            if args['q'] is not "":
                qry = qry.filter_by(nama=args['q'])
                output["pencarian"] = args['q']
                
            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Products.respond_field))
            
            output["page"] = args['p']
            output["total_page"] = 6 # round(Barangs.count()/args['rp'])
            output["per_page"] = args['rp']
            output["hasil"] = rows
            
            return output, 200, {'Content-Text':'application/json'}
        else:
            qry = Products.query.get(id)
            if  qry.client_id != client_id:
                return {"status": "Not Your Product"}, 404, {'Content-Text':'application/json'}

            if qry is not None:
                output["page"] = args['p']
                output["total_page"] = 6 # round(len(Ta)/args['rp'])
                output["per_page"] = args['rp']
                output["hasil"] = marshal(qry, Products.respond_field)
                return output, 200, {'Content-Text':'application/json'} 
        return {"status": "DATA_NOT_FOUND"}, 404, {'Content-Text':'application/json'}

    @jwt_required
    def post(self):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}

        client_id = jwtClaims['id']
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location = 'json')
        parser.add_argument('vendor', location = 'json')
        parser.add_argument('deskripsi', location = 'json')
        parser.add_argument('product_type_id', location = 'json')
        parser.add_argument('price', location = 'json')
        parser.add_argument('status', location = 'json')
        parser.add_argument('url_picture', location = 'json')
        parser.add_argument('qty', location = 'json')

        args = parser.parse_args()

        product = Products(
            None, args['nama'], args['vendor'], args['deskripsi'], args['product_type_id'], args['price'],
            args['status'], args['url_picture'], args['qty'], client_id)
        db.session.add(product)
        db.session.commit()

        return {"status": "Add Success"}, 200, {'Content-Text':'application/json'}

    @jwt_required
    def put(self, id):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}

        parser = reqparse.RequestParser()
        parser.add_argument('nama', location = 'json')
        parser.add_argument('vendor', location = 'json')
        parser.add_argument('deskripsi', location = 'json')
        parser.add_argument('product_type_id', location = 'json')
        parser.add_argument('price', location = 'json')
        parser.add_argument('status', location = 'json')
        parser.add_argument('url_picture', location = 'json')
        parser.add_argument('qty', location = 'json')
        args = parser.parse_args()

        qry = Products.query.get(id)
        if qry is None:
            return {"status": "NOT_FOUND"}, 404, {'Content-Text':'application/json'}
        
        # qry.deskripsi = args['deskripsi']
        if args['nama'] is not None:
            qry.nama = args['nama']
        if args['vendor'] is not None:
            qry.vendor = args['vendor']
        if args['deskripsi'] is not None:
            qry.deskripsi = args['deskripsi']
        if args['product_type_id'] is not None:
            qry.product_type_id = args['product_type_id']
        if args['price'] is not None:
            qry.price = args['price']
        if args['status'] is not None:
            qry.status = args['status']
        if args['url_picture'] is not None:
            qry.url_picture = args['url_picture']
        if args['qty'] is not None:
            qry.qty = args['qty']
        
        db.session.commit()
        return {"status": "Success Updated"}, 200, {'Content-Text':'application/json'}    
    
    @jwt_required
    def delete(self, id):
        jwtClaims = get_jwt_claims()
        if jwtClaims["status"] != "client":
            return {"status": "NOT_FOUND"}, 404, {'Content-Text':'application/json'}
        
        qry = Products.query.get(id)
        if qry is None:
            return {"status": "DATA_NOT_FOUND"}, 404, {'Content-Text':'application/json'}
        db.session.delete(qry)
        db.session.commit()
        return {"status": "Success deleted"}, 200, {'Content-Text':'application/json'}

api.add_resource(ClientProductsResource, '/client/product', '/client/product/<int:id>')

# Buat pengembangan
"""
class ClientProductDescriptionsResource(Resource):

    @jwt_required
    def get(self, id = None):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}
        
        client_id = jwtClaims['id']
        Product_Description = Product_Descriptions.query.filter_by(client_id = client_id)
        if id is None:
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location = 'args', default = 1)
            parser.add_argument('rp', type=int, location = 'args', default = 5)
            parser.add_argument('q', location = 'args', default = "")

            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']
            
            output = dict()
            qry = Product_Description.query
            if args['q'] is not "":
                qry = qry.filter_by(nama=args['q'])
                output["pencarian"] = args['q']
                
            rows = []
            for row in qry.limit(args['rp']).offset(offset).all():
                rows.append(marshal(row, Product_Descriptions.respond_field))
            
            output["page"] = args['p']
            output["total_page"] = 6 # round(Barangs.count()/args['rp'])
            output["per_page"] = args['rp']
            output["hasil"] = rows
            
            return output, 200, {'Content-Text':'application/json'}
        else:
            qry = Product_Description.query.get(id)
            output = dict()
            if qry is not None:
                output["page"] = args['p']
                output["total_page"] = 6 # round(len(Ta)/args['rp'])
                output["per_page"] = args['rp']
                output["hasil"] = marshal(qry, Product_Descriptions.respond_field)
                return output, 200, {'Content-Text':'application/json'} 
        return {"status": "DATA_NOT_FOUND"}, 404, {'Content-Text':'application/json'}

    # @jwt_required
    def post(self):
        # jwtClaims = get_jwt_claims()
        if jwtClaims['status'] is not 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}

        client_id = jwtClaims['id']

        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location = 'json')
        parser.add_argument('berat', location = 'json')
        parser.add_argument('deskripsi', location = 'json')
        args = parser.parse_args()

        qry = Products.query.filter_by(client_id = client_id)
        qry = qry.query.get(args['product_id'])
        if qry is None:
            return {"status": "Invalid product_id"}, 404, {'Content-Text':'application/json'}

        product_description = Product_Descriptions(
            None, args['product_id'], args['berat'], args['deskripsi'])
        db.session.add(product_description)
        db.session.commit()

        return {"status": "Add Success"}, 200, {'Content-Text':'application/json'}

    # @jwt_required
    def put(self, id):
        # jwtClaims = get_jwt_claims()
        if jwtClaims['status'] is not 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}

        client_id = jwtClaims['id']

        parser = reqparse.RequestParser()
        parser.add_argument('product_id', location = 'json')
        parser.add_argument('berat', location = 'json')
        parser.add_argument('deskripsi', location = 'json')
        args = parser.parse_args()

        qry = Product_Descriptions.query.get(id)
        if qry is None:
            return {"status": "NOT_FOUND"}, 404, {'Content-Text':'application/json'}
        
        qry = Products.query.filter_by(client_id = client_id)
        qry = qry.query.get(args['product_id'])
        if qry is None:
            return {"status": "Invalid product_id"}, 404, {'Content-Text':'application/json'}
        
        # qry.deskripsi = args['deskripsi']
        if args['product_id'] is not None:
            qry.product_id = args['product_id']
        if args['berat'] is not None:
            qry.berat = args['berat']
        if args['deskripsi'] is not None:
            qry.deskripsi = args['deskripsi']
        
        db.session.commit()
        return {"status": "Success Updated"}, 200, {'Content-Text':'application/json'}    
    
    # @jwt_required
    def delete(self, id):
        # jwtClaims = get_jwt_claims()
        # if jwtClaims["status"] is not "client":
        #     return {"status": "NOT_FOUND"}, 404, {'Content-Text':'application/json'}
        
        qry = Product_Descriptions.query.get(id)
        if qry is None:
            return {"status": "DATA_NOT_FOUND"}, 404, {'Content-Text':'application/json'}
        db.session.delete(qry)
        db.session.commit()
        return {"status": "Success deleted"}, 200, {'Content-Text':'application/json'}

api.add_resource(ClientProductDescriptionsResource, '/client/product_description', '/client/product_description/<int:id>')

# Buat pengembangan
# Belum jalan
class ClientTransactionDetailsResource(Resource):
    
    @jwt_required
    def get(self, id = None):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}
        
        client_id = jwtClaims['id']

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location = 'args', default = 1)
        parser.add_argument('rp', type=int, location = 'args', default = 5)
        parser.add_argument('q', location = 'args', default = "")

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']
        
        output = dict()
        product = Products.query.filter_by(client_id = client_id)
        # Problem
        qry = Transaction_Details.query.where(product_id in product.id)
        if args['q'] is not "":
            qry = qry.filter_by(nama=args['q'])
            output["pencarian"] = args['q']
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Transaction_Details.respond_field))
        
        output["page"] = args['p']
        output["total_page"] = 6 # Products.query().count()/args['rp'])
        output["per_page"] = args['rp']
        output["hasil"] = rows
        
        return output, 200, {'Content-Text':'application/json'}

api.add_resource(ClientTransactionDetailsResource, '/client/transaction_detail')
"""

class ClientTransactionResource(Resource):
    @jwt_required
    def get(self, product_id):
        jwtClaims = get_jwt_claims()
        if jwtClaims['status'] != 'client':
            return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}

        client_id = jwtClaims['id']
        
        # if id is None:
        #     parser = reqparse.RequestParser()
        #     parser.add_argument('p', type=int, location = 'args', default = 1)
        #     parser.add_argument('rp', type=int, location = 'args', default = 5)

        #     args = parser.parse_args()

        #     offset = (args['p'] * args['rp']) - args['rp']
            
        #     output = dict()
        #     qry = Transactions.query.filter_by(user_id = user_id)
                
        #     rows = []
        #     for row in qry.limit(args['rp']).offset(offset).all():
        #         rows.append(marshal(row, Transactions.respond_field))
            
        #     output["page"] = args['p']
        #     output["total_page"] = 6 # round(Transactions.count()/args['rp'])
        #     output["per_page"] = args['rp']
        #     output["hasil"] = rows
            
        #     return output, 200, {'Content-Text':'application/json'}
        # else:

        product = Products.query.get(product_id)
        if product is None:
            return {"status": "DATA_NOT_FOUND, this id not in your product"}, 404, {'Content-Text':'application/json'}
        qry = Transactions.query.filter_by(product_id = product_id)

        if qry is not None:
            rows = []
            for row in qry.all():
                rows.append(marshal(row, Transactions.respond_field))
                
            return rows, 200, {'Content-Text':'application/json'} 
        return {"status": "DATA_NOT_FOUND"}, 404, {'Content-Text':'application/json'}

api.add_resource(ClientTransactionResource, '/client/transaction/<int:id>')

class ClientProductTypeResource(Resource):
    # @jwt_required
    def get(self, id = None):
        # jwtClaims = get_jwt_claims()
        # if jwtClaims['status'] is not 'client':
        #     return {"status": "Invalid Status"}, 404, {'Content-Text':'application/json'}
    
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location = 'args', default = 1)
        parser.add_argument('rp', type=int, location = 'args', default = 5)
        parser.add_argument('q', location = 'args', default = "")

        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']
        
        output = dict()
        qry = Product_Types.query
        if args['q'] is not "":
            qry = qry.filter_by(nama=args['q'])
            output["pencarian"] = args['q']
            
        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Product_Types.respond_field))
        
        output["page"] = args['p']
        output["total_page"] = 6 # round(Products.count()/args['rp'])
        output["per_page"] = args['rp']
        output["hasil"] = rows
        
        return output, 200, {'Content-Text':'application/json'}

api.add_resource(ClientProductTypeResource, '/client/product_type')