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

# app.config['MYSQL_DATABASE_USER'] = 'u917498081_servicedb'
# app.config['MYSQL_DATABASE_PASSWORD'] = '$|OS8YaC/r5I'
# app.config['MYSQL_DATABASE_DB'] = 'u917498081_INEDATABASE'
# app.config['MYSQL_DATABASE_HOST'] = 'www.taquitosoftware.com.mx'


mysql.init_app(app)







if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG)