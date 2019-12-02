from app import db
from models.blacklist import Blacklist
from models.person import Person
from models.blacklistClassification import BlacklistClassification
from resources.admin.security import AuthRequiredResource
from resources.utils import allowed_file, getDocumentType, fixDocumentNumber
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask import request
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
import status
import pandas as pd
import logging
import numpy as np

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
            response = {'error': str(e)}
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
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST

    def post(self):
        try:
            file = request.files['file']
            if file.filename == '':
                response = {'error' : 'No selected files'}
                return response, status.HTTP_400_BAD_REQUEST
            
            if file and allowed_file(file.filename):
                df = None
                # [documentNumber], fatherLastname, motherLastname, name, sex, [birthDate]
                try:
                    df = pd.read_csv(file, header=None)
                except:
                    df = pd.read_excel(file, header=None)

                n = df[0].size

                response = {}
                response['badIndexes'] = []
                response['badReasons'] = []

                for i in range(n):
                    documentNumber = df[0][i]
                    fatherLastname = df[1][i]
                    motherLastname = df[2][i]
                    name = df[3][i]
                    sex = df[4][i]
                    birthDate = df[5][i]
                    logging.debug(df[0][i], df[1][i], df[2][i], df[3][i], df[4][i], df[5][i])
                    #Obtener firstName y middleName
                    listNames = [x for x in name.split()]
                    firstName = listNames[0]
                    middleName = ""
                    if len(listNames) > 1:
                        middleName = listNames[1]
                    
                    if isinstance(documentNumber, float):
                        if np.isnan(documentNumber):
                            documentNumber = None
                        else:
                            documentNumber = str(int(documentNumber))
                            documentNumber = fixDocumentNumber(documentNumber)
                    else:
                        documentNumber = fixDocumentNumber(documentNumber) 

                    logging.debug(birthDate, type(birthDate))                    

                    if isinstance(birthDate, float):
                        if np.isnan(birthDate):
                            logging.debug("isnan")
                            birthDate = datetime.now() - timedelta(days=7300)
                    
                    if isinstance(birthDate, str):
                        lstDate = birthDate.split("/")
                        dd, mm, yyyy = lstDate[0], lstDate[1], lstDate[2]
                        birthDate = date(yyyy, mm, dd)

                    if not isinstance(birthDate, datetime):
                        birthDate = datetime.now() - timedelta(days=7300)

                    if pd.isnull(birthDate):
                        logging.debug("ES NAT")
                        birthDate = birthDate = datetime.now() - timedelta(days=7300)
                    logging.debug("IMPRIMIENTO BD")
                    logging.debug(birthDate)

                        
                    if documentNumber:
                        blacklist = Blacklist.query.filter_by(documentNumber=documentNumber).first()
                        if blacklist:
                            logging.debug("esta repetido xd")
                            response['badIndexes'].append(i)
                            response['badReasons'].append("Usuario ya registrado en blacklist")
                        else:
                            blacklist = Blacklist(
                                documentNumber=documentNumber,
                                documentType=getDocumentType(documentNumber),
                                active=1,
                                idBlacklistClassification=1
                            )
                            blacklist.add(blacklist)
                            person = Person.query.filter_by(documentNumber=documentNumber).first()
                            if not person:
                                person = Person(
                                    documentNumber=documentNumber,
                                    documentType=blacklist.documentType,
                                    fatherLastname=fatherLastname,
                                    motherLastname=motherLastname,
                                    firstName=firstName,
                                    middleName=middleName,
                                    birthdate=birthDate,
                                    address="Av. Universitaria 1801, Lima 15108, Peru",
                                    nationality="per",
                                    vehicle1Plate="XXX000",
                                    vehicle2Plate="XXX000",
                                    gender="M"
                                )
                                person.add(person)
                    else:
                        person = Person.query.filter_by(
                            firstName=firstName,
                            motherLastname=motherLastname,
                            fatherLastname=fatherLastname
                        ).first()
                        logging.debug("xd")
                        if person:
                            logging.debug("Encontro persona, revisando si hay blacklist registrado")
                            blacklist = Blacklist.query.filter_by(documentNumber=person.documentNumber).first()
                            logging.debug(blacklist)
                            if blacklist:
                                logging.debug("esta repetido xd x2")
                                response['badIndexes'].append(i)
                                response['badReasons'].append("Usuario ya registrado en blacklist")
                            else:
                                blacklist = Blacklist(
                                    documentNumber=person.documentNumber,
                                    documentType=person.documentType,
                                    active=1,
                                    idBlacklistClassification=1
                                )
                                blacklist.add(blacklist)
                        else:
                            response['badIndexes'].append(i)
                            response['badReasons'].append("Usuario sin match en la base de datos")
                logging.debug("todo bien")
                db.session.commit()
                response['ok'] = 'Registros agregados correctamente'
                return response, status.HTTP_200_OK
            else:
                response = {'error' : 'Bad file sent. Please check extension.'}
                return response, status.HTTP_400_BAD_REQUEST

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST

        except Exception as e:
            db.session.rollback()
            response = {'error': str(e)}
            logging.debug(str(e))
            return response, status.HTTP_400_BAD_REQUEST
