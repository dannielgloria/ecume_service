import re
import json
import pymysql
from flask import Flask, request, flash, jsonify
from flaskext.mysql import MySQL

# FLASK Instance my application
app = Flask(__name__)
PORT = 5000
DEBUG = False
mysql = MySQL()

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
    bloodbPressure = json_data['BloodPresure']
    token = hashlib.md5(names+email).digest()
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
    surgicalInterventions = json_data['surgicalInterventions'] 
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
    if ((pH0 = 0) and (pH1 = 0) and (pH2 = 0) and (pH3 = 0) and (pH4 = 0) and (pH5 = 0) and (pH6 = 0) and (activityLevel = 1 or activityLevel = 2) and ((noActivity = 1 or ( lowActivity = 1 or lowActivity = 2)) and (surgicalInterventions = 0) and (fractures = 0) and (hospitalization = 1) and (tobaccoConsumption = 1) and (alcoholConsumption = 0) and (numberOfMeals = 2) and (physicalActivity = 0)):
        group = 1
        cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
        cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
        cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
        cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
        cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
        conn.commit()
        resp = jsonify(cur.rowcount)
        resp.status_code=200
        return resp
        elif ((pH0 = 0) and (pH1 = 0) and (pH2 = 0) and (pH3 = 0) and (pH4 = 0) and (pH5 = 0) and (pH6 = 0) and (activityLevel = 3 or activityLevel = 4) and (lowActivity = 3 or lowActivity = 4) and  (surgicalInterventions = 0) and (fractures = 0) and (hospitalization = 0) and (tobaccoConsumption = 0) and (alcoholConsumption = 0) and (numberOfMeals = 3) and (physicalActivity = 2)):
            group = 2
            cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
            cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
            cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
            cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
            cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
            conn.commit()
            resp = jsonify(cur.rowcount)
            resp.status_code=200
            return resp
            elif ((pH0 = 0) and (pH1 = 0) and (pH2 = 0) and (pH3 = 0) and (pH4 = 0) and (pH5 = 0) and (pH6 = 0) and (activityLevel = 5 or activityLevel = 6) and ((highActivity = 5 or highActivity = 6) or (highActivity = 7)) and (surgicalInterventions = 0) and (fractures = 0) and (hospitalization = 0) and (tobaccoConsumption = 0) and (alcoholConsumption = 0) and (numberOfMeals = 4) and (physicalActivity = 1)):
                group = 3
                cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
                cur.execute('INSERT INTO Lifestyle (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, bath, toothBrushing, sharedRoom, tobaccoConsumption, alcoholConsumption, numberOfMeals, physicalActivity))
                cur.execute('INSERT INTO AttitudeToExercise (email, activityLevel, noActivity, lowActivity, highActivity) VALUES (%s, %s, %s, %s, %s);', (email, activityLevel, noActivity, lowActivity, highActivity))
                cur.execute('INSERT INTO PersonalHistory (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (email, diabetes, hypertension, heartDisease, kidneyDisease, respiratoryDisease, jointDisease, allergies, hyperthyroidism, hypothyroidism, otherDisease, surgicalInterventions, fractures, hospitalization))
                cur.execute('INSERT INTO PhysicalHandicap (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);', (email, pH0, pH1, pH2, pH3, pH4, pH5, pH6))
                conn.commit()
                resp = jsonify(cur.rowcount)
                resp.status_code=200
                return resp
                elif ((((pH0 = 1) or (pH3 = 1)) or (pH5 = 1)) and (activityLevel = 1 or activityLevel = 2) and (noActivity = 1) and  (surgicalInterventions = 1) and (fractures = 1) and (hospitalization = 1) and (tobaccoConsumption = 1) and (alcoholConsumption = 1) and (numberOfMeals = 2) and (physicalActivity = 0)):
                    group = 4
                    cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
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
                    cur.execute('INSERT INTO User (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (token, names, surnames, password, email, phone, height, weight, yearBirth, gender, bloodPressure, group))
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