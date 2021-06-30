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

@app.route('/apiECUME/getAllUsers', methods=['GET'])
def get_allUsers():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM User')
    rows = cur.fetchall()
    resp = jsonify(rows)
    resp.status_code=200
    return resp

@app.route('/apiECUME/login', methods=['POST'])
def get_tokenLogin():
    json_data = request.get_json()
    email = json_data['email']
    password = json_data['password']
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT token FROM User WHERE Email = %s AND Password = %s ;', (email,password))
    rows = cur.fetchone()
    resp = jsonify(rows)
    resp.status_code=200
    return resp

@app.route('/apiECUME/recoverPwd', methods=['GET'])
def get_recoverPassword():
    json_data = request.get_json()
    phone = json_data['phone']
    phone = re.sub(r"[a-zA-Z . +-]+", "" ,phone)
    email = json_data['email']
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT Password FROM User WHERE Phone = %s OR Email = %s;', (phone,email))
    row = cur.fetchone()
    rw = str(row)
    if rw == 'None':
        resp = {"error": "The email or number you entered is incorrect"}
        resp = json.dumps(resp)
        return resp
    else:
        resp = jsonify(row)
        resp.status_code=200
        return resp
    

@app.route('/apiECUME/userRegister', methods=['POST'])
def put_userRegister():
    json_data = request.get_json() 
    names = json_data['names']
    surnames = json_data['surnames']
    password = json_data['password']
    email = json_data['email']
    phone = json_data['phone']
    phone = re.sub(r"[a-zA-Z . +-]+", "" ,phone)
    height = json_data['height']
    weight = json_data['weight']
    yearBirth = json_data['yearBirth']
    gender = json_data['gender']
    bloodPressure = json_data['bloodPresure']
    h = blake2b(key=SECRET_KEY, digest_size=16)
    h.update(str.encode(names+surnames+email))
    # naMail= names+email+str(random.randint(10000, 1000000))
    token = str(h.hexdigest())
    #* Phyisical handicap
    pH0 = json_data['answer1']
    pH1 = json_data['answer2']
    pH2 = json_data['answer3']
    pH3 = json_data['answer4']
    pH4 = json_data['answer5']
    pH5 = json_data['answer6']
    pH6 = json_data['answer7']
    #* Attitude To Exercise
    activityLevel = json_data['activityLevel']
    noActivity = json_data['noActivity']
    lowActivity = json_data['nowActivity']
    highActivity = json_data['highActivity']
    #* Personal History
    diabetes = json_data['diabetes']
    hypertension = json_data['hypertension']
    heartDisease = json_data['heartDisease']
    kidneyDisease = json_data['kidneyDisease']
    respiratoryDisease = json_data['respiratoryDisease']
    jointDisease = json_data['jointDisease']
    allergies = json_data['allergies']
    hyperthyroidism = json_data['hyperthyroidism']
    hypothyroidism = json_data['hypothyroidism']
    otherDisease = json_data['otherDisease']
    surgicalInterventions = json_data['surgicalInterventions'] 
    fractures = json_data['fractures']
    hospitalization = json_data['hospitalization']
    #* Lifestyle
    bath = json_data['bath']
    toothBrushing = json_data['toothBrushing']
    sharedRoom = json_data['sharedRoom']
    tobaccoConsumption = json_data['tobaccoConsumption']
    alcoholConsumption = json_data['alcoholConsumption']
    numberOfMeals = json_data['numberOfMeals']
    physicalActivity = json_data['physicalActivity']
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    phS = (pH0+pH1+pH2+pH3+pH4+pH5+pH6)
    fS = (activityLevel+noActivity+lowActivity+highActivity+surgicalInterventions+fractures+hospitalization+tobaccoConsumption+alcoholConsumption+numberOfMeals+physicalActivity)
    nD = (diabetes+hypertension+heartDisease+kidneyDisease+respiratoryDisease+jointDisease+allergies+hyperthyroidism+hypothyroidism+otherDisease)
    if ( ((phS == 0) and (fS >= 5 and fS <= 7)) and (nD >= 3)):
        group = 1
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        resp = 'User was successfully registered'
        return resp
    elif (((phS == 0) and (fS >= 11 and fS <= 13)) and (nD >= 2 and nD <= 3)):
        group = 2
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        resp = 'User was successfully registered'
        return resp
    elif (((phS == 0) and (fS >= 15 and fS <= 18)) and (nD >= 2 and nD <= 3)):
        group = 3
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        resp = 'User was successfully registered'
        return resp
    elif (phS != 0):
        group = 4
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        resp = 'User was successfully registered'
        return resp
    else:
        group = 5
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, trainingGroup) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        resp = 'User was successfully registered'
        return resp
    
@app.route('/apiECUME/deleteUser', methods=['DELETE'])
def delete_deleteUser():
    json_data = request.get_json()
    email = json_data['Email']
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM AttitudeToExercise WHERE email= %s ;', (email))
    cur.execute('DELETE FROM PhysicalHandicap WHERE email= %s ;', (email))
    cur.execute('DELETE FROM PersonalHistory WHERE email= %s ;', (email))
    cur.execute('DELETE FROM Lifestyle WHERE email= %s ;', (email))
    cur.execute('DELETE FROM User WHERE email= %s ;', (email))
    conn.commit()
    resp = jsonify(cur.rowcount)
    resp.status_code=200
    resp = {"response": "User was successfully deleted"}
    resp = json.dumps(resp)
    return resp

if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)