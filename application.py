import os
import random
import string
import time

import pyodbc as pyodbc
import redis as redis
from flask import Flask, render_template, request
myHostname = "azureassignment3.redis.cache.windows.net"
myPassword = "xw5S6heXPfqGZL4PfzatH+d7nnCawcY5dSMNTyWC+qQ="
server = 'mysqlserversuchitra.database.windows.net'
database = 'assignment3'
username = 'azureuser'
password = 'Geetha1963@'
driver= '{ODBC Driver 17 for SQL Server}'

r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)

app = Flask(__name__)
port = os.getenv('VCAP_APP_PORT','5000')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/records1')
def records1():
    return render_template('records1.html')


@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/select1',methods=['POST', 'GET'])
def select1():
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    start_time = time.time()
    loop = int(request.form['loop'])
    char=request.form['char']
    rows = []
    c = []
    for i in range(loop):
        val = random.choice(string.ascii_lowercase)
        cur = cnxn.cursor()
        net = char + val
        a = "select * from all_month WHERE net = "+net
        if r.get(a):
            #print ('Cached')
            c.append('Cached')
            #print (r.get(a))
            res = r.get(a)
            rows.append(res)
        else:
            #print('Not Cached')
            c.append('Not Cached')
            cur.execute("select * from all_month WHERE net =?",net)
            get = cur.fetchall()
            rows.append(get)
            r.set(a,str(get))
    for i in rows:
        print(i)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", etime=elapsed_time, data=rows)

@app.route('/select2',methods=['POST', 'GET'])
def select2():
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    start_time = time.time()
    loop = int(request.form['loop'])
    char=request.form['char']
    rows = []
    for i in range(loop):
        val = random.choice(string.ascii_lowercase)
        cur = cnxn.cursor()
        net = char + val
        cur.execute("select * from all_month WHERE net =?",net)
        get = cur.fetchall()
        rows.append(get)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", etime=elapsed_time, data=rows)


if __name__ == '__main__':
    app.run()
