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

### API Endpoint Documentation:
**Endpoint 1 - Create Household**:
_localhost:5000/create/household_
POST to the URL with a JSON containing id and housingType
> {"id": 7, "housingType": "Shophouse"}

**Endpoint 2 - Add a family member to household**
_localhost:5000/create/member_
POST to the URL with a JSON containing Name, Gender, Marital Status, ID of Spouse (PK), OccupationType, Annual Income, DOB (YYYY-MM-DD format)
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
_localhost:5000/householdFamily_
GET to the URL for all households and family members in a single JSON

Future Work:
- Containerising into microservice architecture, having family and household functions be in their own containers. Grant calculation will be done through a complex microservice that checks for age and household income.
- Clean up of smelly code where reused code are sorted into a function to be used.
- Unit Tests with pytest for different test cases.
