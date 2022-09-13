from codecs import getencoder
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from jsonmerge import merge

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

