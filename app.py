import re
import json
import random
import pymysql
from hashlib import blake2b
from flask_cors import CORS
from flask import Flask, request, flash, jsonify
from flaskext.mysql import MySQL


# FLASK Instance my application
app = Flask(__name__)
PORT = 5000
DEBUG = True
mysql = MySQL()
cors = CORS(app, resources={r"/*": {"origins": "*"}})
SECRET_KEY=b'3ai6lGjrF*hxy?yzpXN7z*WMnO9rejw7'

##
# Generating the configuration to the connection to the DB
# Change the values of each config according to your credentials from your local DB
##

app.config['MYSQL_DATABASE_USER'] = 'u917498081_ecume'
app.config['MYSQL_DATABASE_PASSWORD'] = '3CUM3d2021!'
app.config['MYSQL_DATABASE_DB'] = 'u917498081_ECUME'
app.config['MYSQL_DATABASE_HOST'] = 'www.taquitosoftware.com.mx'

mysql.init_app(app)

#* This endpoint obtains the record by shaCotejo
@app.route('/apiECUME/login', methods=['GET'])
def get_tokenLogin():
    json_data = request.get_json()
    email = json_data['Email']
    password = json_data['Password']
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT Token FROM User WHERE Email = %s AND Password = %s ;', (email,password))
    rows = cur.fetchall()
    resp = jsonify(rows)
    resp.status_code=200
    return resp

@app.route('/apiECUME/recoverPwd', methods=['GET'])
def get_recoverPassword():
    json_data = request.get_json()
    phone = json_data['Phone']
    phone = re.sub(r"[a-zA-Z . +-]+", "" ,phone)
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT Password FROM User WHERE Phone = %s ;', (phone))
    rows = cur.fetchall()
    resp = jsonify(rows)
    resp.status_code=200
    if resp == '[ ]':
        resp = "Numero no encontrado"
        return resp
    else:
        return resp
    

@app.route('/apiECUME/userRegister', methods=['PUT'])
def put_userRegister():
    json_data = request.get_json() 
    names = json_data['Names']
    surnames = json_data['Surnames']
    password = json_data['Password']
    email = json_data['Email']
    phone = json_data['Phone']
    phone = re.sub(r"[a-zA-Z . +-]+", "" ,phone)
    height = json_data['Height']
    weight = json_data['Weight']
    yearBirth = json_data['YearBirth']
    gender = json_data['Gender']
    bloodPressure = json_data['BloodPresure']
    h = blake2b(key=SECRET_KEY, digest_size=16)
    h.update(str.encode(names+surnames+email))
    # naMail= names+email+str(random.randint(10000, 1000000))
    token = str(h.hexdigest())
    #* Phyisical handicap
    pH0 = json_data['Answer1']
    pH1 = json_data['Answer2']
    pH2 = json_data['Answer3']
    pH3 = json_data['Answer4']
    pH4 = json_data['Answer5']
    pH5 = json_data['Answer6']
    pH6 = json_data['Answer7']
    #* Attitude To Exercise
    activityLevel = json_data['ActivityLevel']
    noActivity = json_data['NoActivity']
    lowActivity = json_data['LowActivity']
    highActivity = json_data['HighActivity']
    #* Personal History
    diabetes = json_data['Diabetes']
    hypertension = json_data['Hypertension']
    heartDisease = json_data['HeartDisease']
    kidneyDisease = json_data['KidneyDisease']
    respiratoryDisease = json_data['RespiratoryDisease']
    jointDisease = json_data['JointDisease']
    allergies = json_data['Allergies']
    hyperthyroidism = json_data['Hyperthyroidism']
    hypothyroidism = json_data['Hypothyroidism']
    otherDisease = json_data['OtherDisease']
    surgicalInterventions = json_data['SurgicalInterventions'] 
    fractures = json_data['Fractures']
    hospitalization = json_data['Hospitalization']
    #* Lifestyle
    bath = json_data['Bath']
    toothBrushing = json_data['ToothBrushing']
    sharedRoom = json_data['SharedRoom']
    tobaccoConsumption = json_data['TobaccoConsumption']
    alcoholConsumption = json_data['AlcoholConsumption']
    numberOfMeals = json_data['NumberOfMeals']
    physicalActivity = json_data['PhysicalActivity']
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    phS = (pH0+pH1+pH2+pH3+pH4+pH5+pH6)
    fS = (activityLevel+noActivity+lowActivity+highActivity+surgicalInterventions+fractures+hospitalization+tobaccoConsumption+alcoholConsumption+numberOfMeals+physicalActivity)
    nD = (diabetes+hypertension+heartDisease+kidneyDisease+respiratoryDisease+jointDisease+allergies+hyperthyroidism+hypothyroidism+otherDisease)
    if ( ((phS == 0) and (fS >= 5 and fS <= 7)) and (nD >= 3)):
        group = 1
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroups) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        return resp
    elif (((phS == 0) and (fS >= 11 and fS <= 13)) and (nD >= 2 and nD <= 3)):
        group = 2
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroups) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        return resp
    elif (((phS == 0) and (fS >= 15 and fS <= 18)) and (nD >= 2 and nD <= 3)):
        group = 3
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroups) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        return resp
    elif (phS != 0):
        group = 4
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroups) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        return resp
    else:
        group = 5
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroups) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        return resp


if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)