import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.auth import *

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateUserTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()
        
        qry = Users.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        if qry != None :
            token = create_access_token(marshal(qry, Users.respond_field))
        else : 
            return {'status':'UNAUTHORIZED', 'message':'invalid key or secret'}, 401
        return {'token': token}, 200

api.add_resource(CreateUserTokenResources, '/token/user')

class CreateAdminTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()
        
        qry = Admins.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        if qry != None :
            token = create_access_token(marshal(qry, Admins.respond_field))
        else : 
            return {'status':'UNAUTHORIZED', 'message':'invalid key or secret'}, 401
        return {'token': token}, 200

api.add_resource(CreateAdminTokenResources, '/token/admin')

class CreateClientTokenResources(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location='args', required=True)
        args = parser.parse_args()
        
        qry = Clients.query.filter_by(username=args['username']).filter_by(password=args['password']).first()
        if qry != None :
            token = create_access_token(marshal(qry, Clients.respond_field))
        else : 
            return {'status':'UNAUTHORIZED', 'message':'invalid key or secret'}, 401
        return {'token': token}, 200

api.add_resource(CreateClientTokenResources, '/token/client')