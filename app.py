from codecs import getencoder
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from jsonmerge import merge
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/govgrantapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

#TODO: Create DB to host household 
class Household(db.Model):
    __tablename__ = 'household'
    id = db.Column(db.Integer, primary_key=True)
    housingType = db.Column(db.String(12), nullable=False)
    familymember = db.relationship('FamilyMember', backref='familymember')

    def __init__(self, id, housingType):
        self.id = id
        self.housingType = housingType

    def json(self):
        return {"id":self.id, "housingType": self.housingType}

class FamilyMember(db.Model):
    __tablename__ = 'familymember'
    id = db.Column(db.Integer, primary_key=True)
    householdId = db.Column(db.Integer, db.ForeignKey('household.id'))
    name = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    maritalStatus = db.Column(db.String(10), nullable=False)
    spouse = db.Column(db.Integer)
    occupationType = db.Column(db.String(10), nullable=False)
    annualIncome = db.Column(db.Integer, nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)

    def __init__(self, id, householdId, name, gender, maritalStatus, spouse, occupationType, annualIncome, dateOfBirth):
        self.id = id
        self.householdId = householdId
        self.name = name
        self.gender = gender
        self.maritalStatus = maritalStatus
        self.spouse = spouse
        self.occupationType = occupationType
        self.annualIncome = annualIncome
        self.dateOfBirth = dateOfBirth
    
    def json(self):
        return {"id": self.id, "householdId": self.householdId, "name": self.name, "gender": self.gender, "maritalStatus": self.maritalStatus, "spouse":self.spouse, "occupationType": self.occupationType, "annualIncome": self.annualIncome, "dateOfBirth": self.dateOfBirth}

#TODO:EP1 Create household
@app.route("/create/household", methods=["GET", "POST"])
def create_household():
    if request.is_json:
        id=request.json['id']
        housingType = request.json['housingType']

        #If household-to-create exists, return error
        if (Household.query.filter_by(id=id).first()):
            return jsonify(
                {
                    "code":400,
                    "data": {
                        "id": id
                    },
                    "message": "Household already exists"
                }
            ), 400
            
        toAdd = Household(id, housingType)

        try:
            db.session.add(toAdd)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "id": id
                    },
                    "message": "An error occurred creating the household"
                    }
            ), 500
        return jsonify({"code": 201, "id": toAdd.id, "housingType": toAdd.housingType}), 201
    return{"code": 400, "message": "Request must be a JSON"}, 400

#TODO: EP2 Add a family member to household
@app.route("/create/member", methods=['GET', 'POST'])
def add_member():
    if request.is_json:
        id=request.json['id']
                #If household-to-create exists, return error
        if (FamilyMember.query.filter_by(id=id).first()):
            return jsonify(
                {
                    "code":400,
                    "data": {
                        "id": id
                    },
                    "message": "Member already exists"
                }
            ), 400

        toAdd = FamilyMember(id, householdId=request.json['householdId'], name=request.json['name'], gender=request.json['gender'], maritalStatus=request.json['maritalStatus'], spouse=request.json['spouse'], occupationType=request.json['occupationType'], annualIncome=request.json['annualIncome'], dateOfBirth=request.json['dateOfBirth'])
        
        try:
            db.session.add(toAdd)
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "id": id
                    },
                    "message": "An error occurred adding family member"
                }
            ), 500
        return jsonify({"code": 201, "id": toAdd.id, "householdId": toAdd.householdId, "name": toAdd.name, "gender": toAdd.gender, "maritalStatus": toAdd.maritalStatus, "spouse": toAdd.spouse, "occupationType": toAdd.occupationType, "annualIncome": toAdd.annualIncome, "dateOfBirth": toAdd.dateOfBirth}), 201
    return {"code": 400, "message": "Request must be a JSON"}, 400

#TODO: EP3 List all households and family data
@app.route("/householdFamily")
def get_householdFamily():
    familyList = FamilyMember.query.all()
    householdList = Household.query.all()
    householdFamily = []

    #IF households exist in Household DB, return list of households
    if len(familyList) and len(householdList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "households":[household.json() for household in householdList],
                    "familyMembers": [familyMember.json() for familyMember in familyList]
                }
            }
        )
    #Else return 404 error, no households found
    return jsonify(
        {
            "code": 404,
            "message": "There are no family members"
        }
    ), 404

#TODO: EP3 - List households only
#TODO: EP3 - List family data only
#TODO: EP3 Household data only
@app.route("/household")
def get_households():
    householdList = Household.query.all()

    #IF households exist in Household DB, return list of households
    if len(householdList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "households": [household.json() for household in householdList]
                }
            }
        )
    #Else return 404 error, no households found
    return jsonify(
        {
            "code": 404,
            "message": "There are no households"
        }
    ), 404

#TODO: EP3 - Family member data only
@app.route("/familymember")
def get_familymembers():
    familyList = FamilyMember.query.all()

    #IF households exist in Household DB, return list of households
    if len(familyList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "familymembers": [family.json() for family in familyList]
                }
            }
        )
    #Else return 404 error, no households found
    return jsonify(
        {
            "code": 404,
            "message": "There are no family members"
        }
    ), 404

#TODO: EP4 - Specific Household in the DB based on ID
@app.route("/getSpecificHousehold")
def get_specificHousehold():
    if request.is_json:
        id=request.json['id']
        familyList = FamilyMember.query.all()
        household = Household.query.filter_by(id=id).first()
        if household:
            return jsonify(
                {
                    "code":200,
                    "household": household.json(),
                    "familyMembers": [familyMember.json() for familyMember in familyList if familyMember.householdId==household.id]
                    }
            )
        return jsonify({
            "code": 404,
            "message": "The household does not exist"
        })
    return jsonify(
        {
            "code": 400,
            "message": "Request should be a JSON"
        }
    )

#TODO: EP5 - Grant Checks - Student Encouragement Bonus
#Check all, return those that have a student that is eligible
@app.route("/studentEncouragementBonus")
def studentBonusEligibility():
    familyList = FamilyMember.query.all()
    householdsJson = get_households().get_json()
    eligibleHouseholds = []
    householdLimit = 200000
    today = date.today()

    for household in householdsJson['data']['households']: 
        householdIncome = 0
        studentEligibilityCheck = False
        qualifyingMembers = []
        houseIdToCheck = household['id']
        familyMembersToCheck = [familyMember.json() for familyMember in familyList if familyMember.householdId==houseIdToCheck]
        # print(familyMembersToCheck)

        #Checking student eligibility and household income
        for member in familyMembersToCheck:
            householdIncome += member['annualIncome']
            if (studentEligibilityCheck == False):
                if member['occupationType'].upper().strip() == "STUDENT":
                    birthDate = member['dateOfBirth']
                    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                    if age < 16:
                        studentEligibilityCheck = True
                        qualifyingMembers.append(member['id'])

        if (householdIncome < householdLimit) and studentEligibilityCheck:
            eligibleHouseholds.append({"householdId": houseIdToCheck, "qualifyingMemberId": qualifyingMembers})

    if eligibleHouseholds == []:
        return jsonify({
            "code": 200,
            "data": "There are no eligible households/qualifying members for this grant scheme"
        })

    return jsonify({
        "code": 200,
        "data": eligibleHouseholds
        })

#TODO: EP 5 - Grant Checks - Multigenerational
@app.route("/multigenerationScheme")
def multigenerationEligibility():
    familyList = FamilyMember.query.all()
    householdsJson = get_households().get_json()
    eligibleHouseholds = []
    householdLimit = 150000
    today = date.today()

    for household in householdsJson['data']['households']: 
        qualifyingMembers = []
        householdIncome = 0
        generationalCheck = False
        houseIdToCheck = household['id']
        familyMembersToCheck = [familyMember.json() for familyMember in familyList if familyMember.householdId==houseIdToCheck]

        for member in familyMembersToCheck:
            qualifyingMembers.append(member['id'])
            householdIncome += member['annualIncome']

            if (generationalCheck == False):
                birthDate = member['dateOfBirth']
                age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
                if (age < 18) or (age > 55):
                    generationalCheck = True
        
        if (householdIncome < householdLimit) and generationalCheck:
            eligibleHouseholds.append({"householdId": houseIdToCheck, "qualifyingMemberId": qualifyingMembers})

    if (eligibleHouseholds == []):
        return jsonify({
            "code": 200,
            "data": "There are no eligible households/qualifying members for this grant scheme"
        })

    return jsonify({
        "code": 200,
        "data": eligibleHouseholds
        })
 
#TODO: EP 5 - Grant Checks - Elder Bonus
@app.route("/elderBonus")
def elderbonusEligibility():
    familyList = FamilyMember.query.all()
    householdsJson = get_households().get_json()
    eligibleHouseholds = []
    today = date.today()

    for household in householdsJson['data']['households']: 
        qualifyingMembers = []
        houseIdToCheck = household['id']
        elderCheck = False
        familyMembersToCheck = [familyMember.json() for familyMember in familyList if familyMember.householdId==houseIdToCheck]

        for member in familyMembersToCheck:
            birthDate = member['dateOfBirth']
            age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
            print(((today.month, today.day) < (birthDate.month, birthDate.day)))

            if (age >= 55):
                qualifyingMembers.append(member['id'])
                elderCheck = True
        
            if (elderCheck):
                eligibleHouseholds.append({"householdId": houseIdToCheck, "qualifyingMemberId": qualifyingMembers})

    if eligibleHouseholds == []:
        return jsonify({
            "code": 200,
            "data": "There are no eligible households/qualifying members for this grant scheme"
        })

    return jsonify({
        "code": 200,
        "data": eligibleHouseholds
    })

#TODO: EP 5 - Grant Checks - Baby Sunshine
@app.route("/babySunshine")
def babySunshineEligibility():
    familyList = FamilyMember.query.all()
    householdsJson = get_households().get_json()
    eligibleHouseholds = []
    today = date.today()

    for household in householdsJson['data']['households']: 
        qualifyingMembers = []
        houseIdToCheck = household['id']
        babyCheck = False
        familyMembersToCheck = [familyMember.json() for familyMember in familyList if familyMember.householdId==houseIdToCheck]

        for member in familyMembersToCheck:
            birthDate = member['dateOfBirth']
            if (birthDate.year == today.year):
                monthAge = today.month - birthDate.month - ((today.day) < (birthDate.day))
                print(monthAge)

                if (monthAge < 8):
                    qualifyingMembers.append(member['id'])
                    babyCheck = True
        
            if (babyCheck):
                eligibleHouseholds.append({"householdId": houseIdToCheck, "qualifyingMemberId": qualifyingMembers})
    if eligibleHouseholds == []:
        return jsonify({
            "code": 200,
            "data": "There are no eligible households/qualifying members for this grant scheme"
        })
    return jsonify({
        "code": 200,
        "data": eligibleHouseholds
    })

#TODO: EP 5 - Grant Checks - YOLO GST Grant
@app.route("/yoloGSTgrant")
def yoloGstEligibility():
    familyList = FamilyMember.query.all()
    householdsJson = get_households().get_json()
    eligibleHouseholds = []
    householdLimit = 100000

    for household in householdsJson['data']['households']: 
        householdIncome = 0
        qualifyingMembers = []
        houseIdToCheck = household['id']
        familyMembersToCheck = [familyMember.json() for familyMember in familyList if familyMember.householdId==houseIdToCheck]

        for member in familyMembersToCheck:
            householdIncome += member['annualIncome']
            qualifyingMembers.append(member['id'])
    
        if householdIncome < householdLimit and qualifyingMembers != []:
            eligibleHouseholds.append({"householdId": houseIdToCheck, "qualifyingMembers": qualifyingMembers})

    if eligibleHouseholds == []:
        return jsonify({
            "code": 200,
            "data": "There are no eligible households/qualifying members for this grant scheme"
        })

    return jsonify({
        "code": 200,
        "data": eligibleHouseholds
    })

#TODO: Containerize on Docker
#TODO: Unit Tests

if __name__ == '__main__':
    #Run app on port 5000, debug mode
    app.run(debug=True, port=5000)