from app import db
from models.person import Person
from resources.admin.security import AuthRequiredResource
from flask_restful import Resource
from flask import request
import status
import pandas as pd
import random, logging
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

class PersonResource(AuthRequiredResource):
	def get(self, id):
		try:
			person = Person.query.get_or_404(id)
			d = person.toJson()
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class PersonListResource(AuthRequiredResource):
	def get(self):
		try:
			persons = Person.query.all()
			d = []
			for person in persons:
				e = person.toJson()
				d.append(e)
			
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
	def post(self):
		try:
			df = pd.read_csv('listaPersonas.txt', header=None)
			n = df[0].size
			for i in range(n):
				documentNumber = df[0][i]
				surnames = df[1][i].split()
				fatherLastname = " ".join(surnames[:-1])
				motherLastname = surnames[-1]
				names = df[2][i].split()
				flag = int(df[3][i])
				firstName = names[0]
				middleName = " ".join(names[1:])
				documentType = "DNI" if flag == 1 else "CARNET DE EXTRANJERIA"
				#9194 7484
				birthDate = datetime.now() - timedelta(days=random.randint(7484,9194))
				address = "Av. Universitaria 1801, Lima 15108, Peru"
				nationality = "per"
				randomPlate = "".join(chr(x) for x in [random.randint(ord('A'), ord('Z')) for _ in range(3)])
				randomPlate += "".join(chr(x) for x in [random.randint(ord('0'),ord('9')) for _ in range(3)])
				vehicle1Plate = randomPlate
				randomPlate = "".join(chr(x) for x in [random.randint(ord('A'), ord('Z')) for _ in range(3)])
				randomPlate += "".join(chr(x) for x in [random.randint(ord('0'),ord('9')) for _ in range(3)])
				vehicle2Plate = randomPlate
				gender = "F" if random.randint(0, 1) == 0 else "M"
				person = Person(
					documentNumber=documentNumber if flag == 1 else ("0000" + str(documentNumber)),
					documentType=documentType,
					fatherLastname=fatherLastname,
					motherLastname=motherLastname,
					firstName=firstName,
					middleName=middleName,
					birthdate=birthDate,
					address=address,
					nationality=nationality,
					vehicle1Plate=vehicle1Plate,
					vehicle2Plate=vehicle2Plate,
					gender=gender
				)
				logging.debug(firstName)
				person.add(person)
				db.session.commit()

			d = {'ok': 'Personas agregadas correctamente'}
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST

class PersonDocumentResource(AuthRequiredResource):
	def post(self):
		requestDict = request.get_json()
		if not requestDict:
			response = {'error': 'No input data provided'}
			return response, status.HTTP_400_BAD_REQUEST
		try:
			documentNumber = requestDict['documentNumber']
			person = Person.query.filter_by(documentNumber=documentNumber).first()
			d = person.toJson()
			return d, status.HTTP_200_OK
		except SQLAlchemyError as e:
			db.session.rollback()
			response = {'error': str(e)}
			return response, status.HTTP_400_BAD_REQUEST
		except Exception as e:
			db.session.rollback()
			response = {'error': 'An error ocurred. Contact cat-support asap. ' + str(e)}
			return response, status.HTTP_400_BAD_REQUEST
