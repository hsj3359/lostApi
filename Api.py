# -- coding: utf-8 --
import sqlite3
import schedule
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False
bossName = ["oreha", "argos", "baltanNomal", "viakissNormal", "baltanHard","viakissHard","kukusaten","abrellshude"]

def findPartyNum(bossName):
    num = 0
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("select {0} from partyTable ".format(bossName))
    temp = returnData(c.fetchall())
    for i in temp:
        if i!='' and int(i) > 99:
            tempData = str(i).replace("99","")
            if num<int(tempData):
                num=i
        elif i !='':
            if int(num) < int(i):
                num=i
    return int(num) +1

def resetDaily():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM dailyTask")

def saveDb(tempArray):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("select * from userTable where name = '{0}'".format(tempArray[0]))
    userData = c.fetchall()
    if (userData == []):
        c.execute("INSERT INTO userTable VALUES('{0}',{1},'{2}',{3})".format(tempArray[0], tempArray[1], tempArray[2],
                                                                             tempArray[3]))
        c.execute("INSERT INTO partyTable(name) VALUES('{0}')".format(tempArray[0]))
    elif (returnData(userData)[0] != tempArray[1]):
        c.execute("UPDATE userTable SET itameLevel = {0} WHERE name = '{1}'".format(tempArray[1], tempArray[0]))


def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


def returnData(data):
    if(type(data)== json or type(data) == bytes ):
        data = data.decode('unicode_escape')
    data = str(data)
    data = data.replace('"', "")
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace("(", "")
    data = data.replace(")", "")
    data = data.replace(" ","")
    data = data.split(',')
    return data

#user

@app.route('/addUser/<name>')
def addUser(name):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("select name from userTable")
    userName = c.fetchall()
    for i in userName:
        if(name in returnData(i)[0]):
            return build_actual_response(jsonify("0"))
    c.execute("insert into originUserTable(name) values('{0}');".format(name))
    return build_actual_response(jsonify("1"))  # 받아온 데이터를 다시 전송

@app.route('/findUser')
def findUser():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT name FROM originUserTable")
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송

@app.route('/sendUserData',methods = ['POST'])
def sendUserData():
    data = request.get_data();
    data = returnData(data)
    count = 0
    tempArray= list()
    for i in data:
        if count%4 == 0 and count != 0:
            saveDb(tempArray)
            tempArray = list()
        tempArray.append(i)
        count = count+ 1
        if count == len(data)-1:
           saveDb(tempArray)

    return build_actual_response(jsonify(""))  # 받아온 데이터를 다시 전송

@app.route('/login/<name>')
def login(name):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT origin FROM userTable where name = '{0}'".format(name))
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송

@app.route('/userData')
def userData():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM userTable ORDER by itameLevel DESC ")
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송

@app.route('/user/<origin>')
def user(origin):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM userTable where origin = {0}".format(origin))
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송

@app.route('/removeUSerTable')
def removeUserTable():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    conn.execute("DELETE FROM userTable").rowcount
    return 0  # 받아온 데이터를 다시 전송

@app.route('/getOriginData/<origin>')
def getOriginData(origin):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM userTable where origin = {0} order by itameLevel".format(origin))
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송

@app.route('/updateUser', methods = ['POST'])
def updateUser():
    data = request.get_data();
    data = returnData(data)
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()

    c.execute("UPDATE userTable SET itameLevel = {0} WHERE name = '{1}'".format(data[0],data[1]))
    return  "0" # 받아온 데이터를 다시 전송

#party
@app.route('/searchCreatePartyMember/')
def searchCreatePartyMember():
    temp = request.args.get('bossName', "user01")
    temp1 = request.args.get('bossLevel1', "평택시")
    temp2 = request.args.get('bossLevel2', "평택시")
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT userTable.name,userTable.itameLevel,userTable.job, userTable.origin from userTable left outer join partyTable on userTable.name=partyTable.name where partyTable.{0} =0 and userTable.itameLevel < {2} AND userTable.itameLevel >={1} ORDER by userTable.itameLevel DESC".format(temp,temp1,temp2))
    return build_actual_response(jsonify(c.fetchall())) # 받아온 데이터를 다시 전송

@app.route('/party')
def party():
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM partyReservationTable")
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송


@app.route('/searchPartyAll/<origin>')
def searchPartyAll(origin):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute(
        "select userTable.name, userTable.itameLevel, userTable.job , partyTable.oreha,partyTable.argos,partyTable.baltanNomal,partyTable.viakissNomal,partyTable.baltanHard,partyTable.viakissHard,partyTable.kukusaten,partyTable.abrellshude  from userTable left outer join partyTable on userTable.name = partyTable.name WHERE userTable.origin ={0}".format(
            origin))
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송


@app.route('/searchPartyTobossNameAll/')
def searchPartyTobossNameAll():
    temp0 = request.args.get('origin', "평택시")
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    temp = []
    c.execute("select name from userTable WHERE origin = {0}".format(temp0))
    userName = c.fetchall()
    userCount = 0
    for i in userName:
        for j in bossName:
            c.execute("select userTable.name, userTable.itameLevel, userTable.job , partyTable.{1}  from userTable left outer join partyTable on userTable.name = partyTable.name WHERE userTable.name ='{0}' and partyTable.{1} != 0 ".format(userName[userCount][0], j))
            temp.append(c.fetchall())
            temp.append(j)
        userCount = userCount +1
    return build_actual_response(jsonify(temp))  # 받아온 데이터를 다시 전송

@app.route('/searchPartyTobossName/')
def searchPartyTobossName():
    temp = request.args.get('bossName', "user01")
    temp1 = request.args.get('origin', "평택시")
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("select userTable.name, userTable.itameLevel, userTable.job , partyTable.{0}  from userTable left outer join partyTable on userTable.name = partyTable.name WHERE userTable.origin = {1} and partyTable.{0} != 0 ".format(temp, temp1))
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송


@app.route('/searchPartyToUserName/<userName>')
def searchPartyToUserName(userName):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    temp = []
    for i in bossName:
        c.execute(
            "select userTable.itameLevel, userTable.job , partyTable.{0}  from userTable left outer join partyTable on userTable.name = partyTable.name WHERE userTable.name = '{1}' and partyTable.{0} != 0 ".format(
                i,userName))
        temp.append(c.fetchall())
        temp.append(i)
    return build_actual_response(jsonify(temp))  # 받아온 데이터를 다시 전송

@app.route('/searchParty/')
def searchParty():
    temp = request.args.get('bossName', "user01")
    temp1 = request.args.get('partyNum', "평택시")
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("select userTable.name, userTable.itameLevel, userTable.job  from userTable left outer join partyTable on userTable.name = partyTable.name WHERE partyTable.{0}='{1}' ".format(temp, temp1))
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송


@app.route('/createPartyGet/')
def createPartyGet():
    temp = request.args.get('bossName', "user01")
    temp1 = request.args.get('userName', "평택시")
    temp1 = returnData(temp1)
    temp2 = request.args.get("date","9999")
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    partyNum = findPartyNum(temp)
    for i in temp1:
        c.execute("update partyTable set {0}={1} where name = '{2}'".format(temp, partyNum, i))
    c.execute("insert into partyReservationTable VALUES('{0}',{1},'{2}')".format(temp,partyNum,temp2))

    return build_actual_response(jsonify(""))  # 받아온 데이터를 다시 전송


@app.route('/createParty', methods = ['POST'])
def createParty():
    data = request.get_data();
    data = returnData(data)
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET "+bossName[int(data[0])]
    c.execute(tamp+" = ? WHERE name = ?",(data[1],data[2]))
    return  "0" # 받아온 데이터를 다시 전송

@app.route('/clear', methods = ['POST'])
def clear():
    data = request.get_data();
    data = returnData(data)
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET {0} = 99{1} WHERE {0} = {1}".format(bossName[int(data[0])],data[1])
    c.execute(tamp)
    return  "0" # 받아온 데이터를 다시 전송

@app.route('/clearGET/')
def clearGET():
    temp = request.args.get('bossName', "user01")
    temp1 = request.args.get('partyNum', "평택시")
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("UPDATE partyTable SET {0} = 99{1} WHERE {0} = {1}".format(temp,temp1))
    c.execute("UPDATE partyReservationTable SET partyNum = 99{1} WHERE bossName = '{0}' and partyNum={1}".format(temp,temp1))

    return build_actual_response(jsonify("")) # 받아온 데이터를 다시 전송

@app.route('/clearToName/')
def clearToName():
    temp = request.args.get('bossName', "user01")
    temp1 = request.args.get('userName', "평택시")
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET {0} = 990 WHERE name = {1}".format(temp, temp1)
    c.execute(tamp)
    return  "0" # 받아온 데이터를 다시 전송



@app.route('/clearCancel', methods = ['POST'])
def clearCancel():
    data = request.get_data();
    data = returnData(data)
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET {0} = {1} WHERE {0} = 99{1}".format(bossName[int(data[0])],data[1])
    c.execute(tamp)
    return  "0" # 받아온 데이터를 다시 전송

@app.route('/remove', methods = ['POST'])
def remove():
    data = request.get_data();
    data = returnData(data)
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    tamp = "UPDATE partyTable SET {0} = 0 WHERE name = '{1}'".format(bossName[int(data[0])],data[1])
    c.execute(tamp)
    return  "0" # 받아온 데이터를 다시 전송
#daily
@app.route('/dailyCheck/<userName>')
#일일 컨텐츠 하는애들 전송
def dailyCheck(userName):
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    c.execute("select userTable.name, userTable.itameLevel, userTable.job ,dailyTask.chaos, dailyTask.guardian, dailyTask.epona, dailyTask.viewData  from userTable left outer join dailyTask on userTable.name = dailyTask.name WHERE dailyTask.viewData=0 AND userTable.origin = {0};".format(userName))
    return build_actual_response(jsonify(c.fetchall()))  # 받아온 데이터를 다시 전송

@app.route('/removeDaliyCheck', methods = ['POST'])
#일일 컨텐츠 취소
def removeDaliyCheck():
    data = request.get_data();
    data = returnData(data)
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    for i in data:
        c.execute("UPDATE dailyTask SET viewData = 1 WHERE name = '{0}'".format(i))
    return ""  # 받아온 데이터를 다시 전송

@app.route('/makeDaliyCheck', methods = ['POST'])
#일일 컨텐츠 만들기
def makeDaliyCheck():
    data = request.get_data();
    data = returnData(data)
    conn = sqlite3.connect("lostParty.db", isolation_level=None)
    c = conn.cursor()
    for i in data:
        c.execute("UPDATE dailyTask SET viewData = 0 WHERE name = '{0}'".format(i))
    return ""  # 받아온 데이터를 다시 전송


if __name__ == '__main__':
    app.run(debug=True)
