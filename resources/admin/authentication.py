from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from resources.utils import passwordPolicy
from flask import request, jsonify, make_response, g
from app import db
from resources.admin.security import VerifyPassword
import status
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

class SignupResource(Resource):
    def post(self):
        requestDict = request.get_json()
        if not requestDict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        email = requestDict['email']
        password = requestDict['password']

        user = User.query.filter_by(email=email).first()
        
        #Check if user with same email exists
        if user:
            resp = {"error": "Email address already exists."}
            return resp, status.HTTP_400_BAD_REQUEST

        #Check password strength
        if len(passwordPolicy.test(password)):
            resp = {"error": "Please check password strength. It should have at least 5 characters, 1 uppercase letter, 1 number and 1 special character."}
            return resp, status.HTTP_400_BAD_REQUEST

        newUser = User(email=email, password=generate_password_hash(password, method='sha256'))

        try:
            db.session.add(newUser)
            db.session.commit()

            user = User.query.filter_by(email=email).first()
            g.user = user
            token = g.user.GenerateAuthToken()
            
            d = {}
            
            d['email'] = user.email
            d['id'] = user.id
            
            resp = {'token' : token.decode('ascii')}
            resp.update(d)
            return resp, status.HTTP_200_OK
        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class LoginResource(Resource):
    def post(self):
        requestDict = request.get_json()
        if not requestDict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        email = requestDict['email']
        password = requestDict['password']
        remember = True if requestDict['remember'] else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            resp = {'error': 'Please check your login credentials and try again.'}
            return resp, status.HTTP_400_BAD_REQUEST

        g.user = user
        token = g.user.GenerateAuthToken()
        d = {}
        d['email'] = user.email
        d['id'] = user.id
        d['name'] = 'Jossi Huarcaya'
        d['code'] = 'XX2019'

        resp = {'token' : token.decode('ascii')}
        resp.update(d)
        return resp, status.HTTP_200_OK

class VerifyTokenResource(Resource):
    def get(self):
        requestDict = request.get_json()
        if not requestDict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        
        token = requestDict['token']
        valid = VerifyPassword(token, "unused")
        resp = {'valid': valid}
        return resp, status.HTTP_200_OK

class VerifyEmailResource(Resource):
    def post(self):
        requestDict = request.get_json()
        if not requestDict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST

        user = User.query.filter_by(email=requestDict['email']).first()
        if not user:
            response = {'error': 'El cliente no esta en la base de datos'}
            return response, status.HTTP_400_BAD_REQUEST
        
        g.user = user
        token = g.user.GenerateAuthToken()
        d = {}
        d['email'] = user.email
        d['id'] = user.id

        resp = {'token' : token.decode('ascii')}
        resp.update(d)
        return resp, status.HTTP_200_OK