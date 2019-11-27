from app import db
from models.blacklist import Blacklist
from models.person import Person
from models.blacklistClassification import BlacklistClassification
from resources.admin.security import AuthRequiredResource
from resources.utils import allowed_file
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
from werkzeug.utils import secure_filename
import status
import pandas as pd

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
            if (blacklistClassification is None):
                #Si no está la clasificación
                blacklistClassification = BlacklistClassification(name="Regular",description=reason,active=1)
                blacklistClassification.add(blacklistClassification)

                db.session.flush()

                blacklist = Blacklist(documentType="DNI",documentNumber=dni,active=1,idBlacklistClassification=blacklistClassification.id)
                blacklist.add(blacklist)
                
                db.session.commit()

                response = {'ok': 'Añadido a la Blacklist correctamente'}
                return response, status.HTTP_201_CREATED

            blClassification = BlacklistClassification.query.filter_by(description=reason).first()
            blClassification = blacklistClassification.toJson()
            blacklist = Blacklist(documentType="DNI",documentNumber=dni,active=1,idBlacklistClassification=blClassification['idBlacklistClassification'])
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
            
            file = request.files['file']
            if file.filename == '':
                response = {'error' : 'No selected files'}
                return response, status.HTTP_400_BAD_REQUEST
            
            if file and allowed_file(file.filename):
                df = None
                try:
                    df = pd.read_csv(file.data, header=0, skip_blank_lines=True, 
                         skipinitialspace=True, encoding='latin-1')
                except:
                    df = pd.read_excel(data, header=0)
                
                print(df[0], df[1], df[2])

                return response, status.HTTP_200_OK
            else:
                response = {'error' : 'Bad file sent. Please check extension.'}
                return response, status.HTTP_400_BAD_REQUEST

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error', str(e)}
            return response, status.HTTP_400_BAD_REQUEST
