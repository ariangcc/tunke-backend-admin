import random
from models.person import Person
from models.securityQuestion import SecurityQuestion
from flask_restful import Resource
from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError
import status
from app import db

class SecurityQuestionResource(Resource):
    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'error': 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        
        try:
            idPerson = request_dict['idPerson']
            questionsCount = len(SecurityQuestion.query.all())
            questionsIdPool = [x for x in range(1, questionsCount + 1)]
            d = {}
            d['securityQuestions'] = []
            for totalQuestions in range(3):
                randomPosition = random.randint(0, len(questionsIdPool) - 1)
                idSecurityQuestion = questionsIdPool[randomPosition]
                questionsIdPool.remove(idSecurityQuestion)
                securityQuestion = SecurityQuestion.query.get_or_404(idSecurityQuestion)
                answers, correctAnswerIndex = SecurityQuestion.getAnswers(idSecurityQuestion, idPerson)

                e = {}
                e['idSecurityQuestion'] = idSecurityQuestion
                e['question'] = securityQuestion.question
                e['answers'] = answers
                e['correctAnswerIndex'] = correctAnswerIndex
                d['securityQuestions'].append(e)
            
            return d, status.HTTP_200_OK

        except SQLAlchemyError as e:
            db.session.rollback()
            response = {'error': str(e)}
            return response, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            response = {'error': 'An unexpected error occurred. Please, contact cat-support asap :\'v. ' + str(e) }
            return response, status.HTTP_400_BAD_REQUEST