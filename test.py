import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.parse
import json
import requests
import datetime


def returnData(data):
    data = data.replace('"', "")
    data = data.replace('\n', "")
    data = data.replace(' ', "")
    data = data.replace("[", "")
    data = data.replace("]", "")
    data = data.replace("(", "")
    data = data.replace(")", "")
    data = data.split(',')
    return data

def returnText(data):
    data = re.sub('<.+?>', '', data, 0).strip()
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.replace('Lv.', '')
    data = data.replace(',', '')
    return  data

def getName():
    name= requests.get("http://3359jun.pythonanywhere.com/findUser").text
    name = returnData(name)
    return  name

def getCharacter(name):
    changeName = urllib.parse.quote(name)
    html = urlopen("https://lostark.game.onstove.com/Profile/Character/" + changeName)
    bsObject = BeautifulSoup(html, "html.parser")
    nickName = bsObject.select('#expand-character-list > ul >li>span>button>span')
    return nickName

def searchCharacter(nickName,i):
    changeNickName =  urllib.parse.quote(nickName)
    html = urlopen("https://lostark.game.onstove.com/Profile/Character/" + changeNickName)
    bsObject = BeautifulSoup(html, "html.parser")
    itameLevel = str(bsObject.select('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__item > span:nth-child(2)'))
    itameLevel = returnText(itameLevel)
    itameLevel = itameLevel[0:itameLevel.find('.')]
    level = str( bsObject.select('#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__item > span:nth-child(2)'))
    level = returnText(level)
    job =str([imgData.find('img')['alt'] for imgData in bsObject.select('#lostark-wrapper > div > main > div > div.profile-character-info')])
    job = job.replace('[', '')
    job = job.replace(']', '')
    job = job.replace("'", "")
    print(level)
    if int(level) >= 50:
        data = [nickName, int(itameLevel), job, i]
        return data

def getData(a,b,name):
    tampTotal = list()
    for i in range(a,b):
        character = getCharacter(name[i])
        for j in character:
            data = searchCharacter(j.text, i)
            if data != None:
                tampTotal.append(data)
    return tampTotal



now = datetime.datetime.now()
current_time = now.strftime("%M")
name = getName()
num = int(len(name)/3)

if int(current_time)<=20:
    total = getData(0,num,name)
elif int(current_time) <=40:
    total = getData(num,num*2,name)
else:
    total = getData(num*2, len(name), name)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()
tempArray = []
tempArray.append(str(now))
total.append(tempArray)
print(total)
with open(os.path.join(BASE_DIR, 'news.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(total, json_file, ensure_ascii = False, indent='\t')
res = requests.post("http://3359jun.pythonanywhere.com/sendUserData", data=json.dumps(total))