from app import db
from models.blacklist import Blacklist
from models.person import Person
from models.blacklistClassification import BlacklistClassification
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
import status

class BlackListResource(AuthRequiredResource):
    def post(self):
        try:
            requestDict = request.get_json()
            if not requestDict:
                response = {'error' : 'No input data provided'}
                return response, status.HTTP_400_BAD_REQUEST

            dni = requestDict['dni']
            reason = requestDict['reason']
            blackLists = Blacklist.query.all()
            for bl in blackLists:
                if(dni==bl.documentNumber):
                    response = {'error' : 'Esta persona ya se encuentra en la blackList'}
                    return response, status.HTTP_400_BAD_REQUEST

            blacklistClassification = BlacklistClassification.query.filter_by(description=reason).first()
            blacklistClassification = blacklistClassification.toJson()
            blacklist = Blacklist(documentType="DNI",documentNumber=dni,active=1,idBlacklistClassification=blacklistClassification['idBlacklistClassification'])
            blacklist.add(blacklist)

            db.session.commit()
            
            response = {'ok': 'Añadido a la Blacklist correctamente'}
            return response, status.HTTP_201_CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
            return response, status.HTTP_400_BAD_REQUEST

class BlackListListResource(AuthRequiredResource):
    def get(self):
        try:
            listBlackList = Blacklist.query.all()
            d = []
            for bl in listBlackList:
                bl = bl.toJson()
                blacklistClassification = BlacklistClassification.query.get(bl['idBlacklistClassification'])
                person = Person.query.filter_by(documentNumber=bl['documentNumber']).first()
                e = {}
                e.update(person.toJson())
                e['reason'] = blacklistClassification.description
                d.append(e)
            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

    def post(self):
        try:
            requestDict = request.get_json()
            if not requestDict:
                response = {'error' : 'No input data provided'}
                return response, status.HTTP_400_BAD_REQUEST
            blackLists = Blacklist.query.all()
            for person in requestDict:
                flag = 0
                dni = person['dni']
                for bl in blackLists:
                    if(dni==bl.documentNumber):
                        flag = 1
                        break
                if(flag==1):
                     continue
                motivo = person['motivo']
                blacklistClassification = BlacklistClassification.query.filter_by(description=motivo).first()
                blacklistClassification = blacklistClassification.toJson()
                blacklist = Blacklist(documentType="DNI",documentNumber=dni,active=1,idBlacklistClassification=blacklistClassification['idBlacklistClassification'])
                blacklist.add(blacklist)
            
            db.session.commit()
            response = {'ok' : 'BlackList actualizada correctamente'}
            return response, status.HTTP_201_CREATED

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST