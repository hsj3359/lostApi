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

def main():
    name= requests.get("http://3359jun.pythonanywhere.com/findUser").text
    tampTotal = list()
    name = returnData(name)
    print(name)
    for i in range(0, len(name)):
        print(name[i])
        changeName = urllib.parse.quote(name[i])
        html = urlopen("https://lostark.game.onstove.com/Profile/Character/" + changeName)
        bsObject = BeautifulSoup(html, "html.parser")
        nickName = bsObject.select('#expand-character-list > ul >li>span>button>span')
        for j in nickName:
            changeName = urllib.parse.quote(j.text)
            html = urlopen("https://lostark.game.onstove.com/Profile/Character/" + changeName)
            bsObject = BeautifulSoup(html, "html.parser")
            nickName = j.text
            itamLevel =str( bsObject.select(
                '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__item > span:nth-child(2)'))

            itamLevel = re.sub('<.+?>', '', itamLevel, 0).strip()
            itamLevel = itamLevel.replace('[','')
            itamLevel = itamLevel.replace(']','')
            itamLevel = itamLevel.replace('Lv.','')
            itamLevel = itamLevel.replace(',','')
            itamLevel = itamLevel[0:itamLevel.find('.')]
            level =str( bsObject.select(
                '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__item > span:nth-child(2)'))
            level = re.sub('<.+?>', '', level, 0).strip()
            level = level.replace('[','')
            level = level.replace(']','')
            level = level.replace('Lv.','')
            job =str([imgData.find('img')['alt'] for imgData in
                   bsObject.select('#lostark-wrapper > div > main > div > div.profile-character-info')])
            job = job.replace('[','')
            job = job.replace(']','')
            job = job.replace("'","")
            if int(level) >=50:
                data = [nickName, int(itamLevel), job, i]
                tampTotal.append(data)
    return tampTotal

total = main()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()
tempArray = []
tempArray.append(str(now))
total.append(tempArray)
with open(os.path.join(BASE_DIR, 'news.json'), 'w+',encoding='utf-8') as json_file:
    json.dump(total, json_file, ensure_ascii = False, indent='\t')

res = requests.post("http://3359jun.pythonanywhere.com/sendUserData", data=json.dumps(total))