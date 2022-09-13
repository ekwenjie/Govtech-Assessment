# Govtech-Assessment
### METEOR: Q2 - Grant Disbursement API (Backend Technical Assessment)

The following tools and modules are used to create this project. Please have them installed on your laptop to ensure smooth testing.

Tools used:
- Python 3.7
- WAMPSERVER
- PHPMyAdmin
- Postman
- MySQL

Modules:
- Flask
- SQLAlchemy
- flask_cors
- datetime

### Setup Instructions:
1. Start and have WAMP running
2. Navigate to localhost -> phpmyadmin (comes together with WAMP)
3. Run the govtechGrantAPI.sql file either through importing or copy and pasting the SQL code into the SQL input
4. Navigate to the app.py file on terminal and run using the command: python -m run flask
5. The app will start on port 5000. Testing can then be done on Postman.

### Assumptions:
- A household can contain 0 people, but will not be considered for grant schemes.
- Age calculation is considered down to the day (e.g 8 month and 1 day old baby will not be considered for the Baby Sunshine grant)
- Grant disbursement endpoints are individual endpoints to be called 

### API Endpoint Documentation:
**Endpoint 1 - Create Household**:
_localhost:5000/create/household_
POST to the URL with a JSON containing id and housingType
> {"id": 7, "housingType": "Shophouse"}

**Endpoint 2 - Add a family member to household**
_localhost:5000/create/member_
POST to the URL with a JSON containing Name, Gender, Marital Status, ID of Spouse (PK), OccupationType, Annual Income, DOB (YYYY-MM-DD format)
Example of JSON to post:
> {
    "id" : "9",
    "householdId": 7,
    "name": "Tom",
    "gender": "M",
    "maritalStatus": "Single",
    "spouse": null,
    "occupationType": "Student",
    "annualIncome": 1000,
    "dateOfBirth": "2000-09-09"
}

**Endpoint 3: List all households, all family members**
_localhost:5000/householdFamily_ OR _localhost:5000/household_ OR _localhost:5000/familymember_
GET to the URL for all households and family members in a single JSON or households ONLY or family members ONLY
Example of data returned:
> {
    "code": 200,
    "data": {
        "familyMembers": [
            {
                "annualIncome": 0,
                "dateOfBirth": "Mon, 01 Jan 1990 00:00:00 GMT",
                "gender": "M",
                "householdId": 1,
                "id": 1,
                "maritalStatus": "Single",
                "name": "Yolo Alex",
                "occupationType": "Student",
                "spouse": null
            }
        ],
        "households": [
            {
                "housingType": "Condominium",
                "id": 1
            }
            ]
    }
}

**Endpoint 4: Search for a specific household** 
_localhost:5000/getSpecificHousehold_
GET to the URL with a JSON containing the household id sent
Example of JSON to submit:
> {"id": 4"} 


Example of data returned:
> {
    "code": 200,
    "familyMembers": [
        {
            "annualIncome": 0,
            "dateOfBirth": "Fri, 01 Jan 2010 00:00:00 GMT",
            "gender": "M",
            "householdId": 4,
            "id": 4,
            "maritalStatus": "Single",
            "name": "StudentBonus",
            "occupationType": "Student",
            "spouse": null
        }
    ],
    "household": {
        "housingType": "Mansion",
        "id": 4
    }
}

**Endpoint 5: Check and list all households and qualifying members for grant schemes**
_localhost:5000/studentEncouragementBonus_ **OR** _localhost:5000/multigenerationScheme_ **OR** _localhost:5000/elderBonus_ **OR** _localhost:5000/babySunshine_ **OR** _localhost:5000/yoloGSTgrant_
GET to the URL depending on the respective grant schemes to find the eligible households and qualifying members
Example of JSON returned:
> {
    "code": 200,
    "data": [
        {
            "householdId": 2,
            "qualifyingMemberId": [
                6
            ]
        }
    ]
}

### Future Work:
- Containerising into microservice architecture, having family and household functions be in their own containers. Grant calculation will be done through a complex microservice that checks for age and household income.
- Clean up of smelly code where reused code are sorted into a function to be used.
- Unit Tests with pytest for different test cases.
