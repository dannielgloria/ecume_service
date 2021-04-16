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





if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)