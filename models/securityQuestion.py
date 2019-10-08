import random
from app import db
from models.utils import AddUpdateDelete
from models.person import Person

class SecurityQuestion(db.Model, AddUpdateDelete):
    __tablename__ = 'securityQuestion'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))

    @staticmethod
    def getAnswers(idQuestion, idPerson):
        person = Person.query.get_or_404(idPerson)
        answers = [""] * 4
        correctAnswerIndex = random.randint(0, 3) 
        if idQuestion == 1: # Que numero de placa tiene tu auto?
            vehicleChoose = random.randint(0, 1)
            answers[correctAnswerIndex] = (person.vehicle1Plate if vehicleChoose else person.vehicle2Plate)
            for i in range(4):
                if(i == correctAnswerIndex):
                    continue
                randomPlate = "".join(chr(x) for x in [random.randint(ord('A'), ord('Z')) for _ in range(3)])
                randomPlate += "".join(chr(x) for x in [random.randint(ord('0'),ord('9')) for _ in range(3)])

                answers[i] = randomPlate
        
        if idQuestion == 2: #Cual es la ultima letra de tu segundo apellido?
            answers[correctAnswerIndex] = person.motherLastname[-1:].upper()
            letterPool = [chr(x) for x in range(ord('A'), ord('Z')) if x != ord(answers[correctAnswerIndex])]
            for i in range(4):
                if(i == correctAnswerIndex):
                    continue
                randomPosition = random.randint(0, len(letterPool) - 1)
                randomLetter = "" + letterPool[randomPosition]
                answers[i] = randomLetter
                letterPool.remove(randomLetter)

        if idQuestion == 3: #Cual es el anho anterior a tu nacimiento?
            birthyear = int(person.birthdate.strftime('%Y'))
            answers[correctAnswerIndex] = str(birthyear - 1)
            yearPool = [str(x) for x in range(birthyear - 5, birthyear + 5) if x != (birthyear - 1)]
            for i in range(4):
                if(i == correctAnswerIndex):
                    continue
                randomPosition = random.randint(0, len(yearPool) - 1)
                randomYear = "" + yearPool[randomPosition]
                answers[i] = randomYear
                yearPool.remove(randomYear)
            
        if idQuestion == 4: #Cual es la suma de tu dia y mes de nacimiento?
            birthday = int(person.birthdate.strftime('%d'))
            birthmonth = int(person.birthdate.strftime('%m'))
            answers[correctAnswerIndex] = str(birthday + birthmonth)
            sumPool = [str(x) for x in range(2, 44) if x != birthday + birthmonth]
            for i in range(4):
                if(i == correctAnswerIndex):
                    continue
                randomPosition = random.randint(0, len(sumPool) - 1)
                randomSum = "" + sumPool[randomPosition]
                answers[i] = randomSum
                sumPool.remove(randomSum)

        return answers, correctAnswerIndex

        

