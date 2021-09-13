# -- coding: utf-8 --
import sqlite3

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

bossName =["orehaNomal","orehaHard","argos1","argos2","argos3","baltanNomal","viakissNomal","baltanHard","viakissHard"]

@app.route('/user')
def user():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM userTable")
    return jsonify(c.fetchall())  # 받아온 데이터를 다시 전송


@app.route('/party')
def party():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM partyTable")
    return jsonify(c.fetchall())  # 받아온 데이터를 다시 전송


@app.route('/createParty', methods = ['POST'])
def createParty():
    data = request.get_data();
    data = data.decode('unicode_escape')
    data = data.replace('"',"")
    data = data.replace("[","")
    data = data.replace("]","")
    data = data.split(',')
    print(data[0])
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET "+bossName[int(data[0])]
    c.execute(tamp+" = ? WHERE name = ?",(data[1],data[2]))
    return  "0" # 받아온 데이터를 다시 전송

@app.route('/clear', methods = ['POST'])
def clear():
    data = request.get_data();
    data = data.decode('unicode_escape')
    data = data.replace('"',"")
    data = data.replace("[","")
    data = data.replace("]","")
    data = data.split(',')
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET {0} = 99{1} WHERE {0} = {1}".format(bossName[int(data[0])],data[1])
    print(tamp)
    c.execute(tamp)
    return  "0" # 받아온 데이터를 다시 전송

@app.route('/clearCancel', methods = ['POST'])
def clearCancel():
    data = request.get_data();
    data = data.decode('unicode_escape')
    data = data.replace('"',"")
    data = data.replace("[","")
    data = data.replace("]","")
    data = data.split(',')
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET {0} = {1} WHERE {0} = 99{1}".format(bossName[int(data[0])],data[1])
    print(tamp)
    c.execute(tamp)
    return  "0" # 받아온 데이터를 다시 전송

@app.route('/remove', methods = ['POST'])
def remove():
    data = request.get_data();
    data = data.decode('unicode_escape')
    data = data.replace('"',"")
    data = data.replace("[","")
    data = data.replace("]","")
    data = data.split(',')
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET {0} = 0 WHERE name = '{1}'".format(bossName[int(data[0])],data[1])
    print(tamp)
    c.execute(tamp)
    return  "0" # 받아온 데이터를 다시 전송



if __name__ == '__main__':
   app.run(debug=True)
