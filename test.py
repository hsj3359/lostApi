import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.parse
import sqlite3


def main():
    name = ["메난민받아주세요", "에플릿", "미래의미중년", "쓸데없이멋있는모코코", "12글자나되니까꽉채웠음", "발헤임할꺼에요", "아리아나그렇죠", "아이스바닐라커피"]
    tampTotal = list()
    for i in range(0, len(name)):
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


conn = sqlite3.connect("lostParty.db", isolation_level=None)
c = conn.cursor()
conn.execute("DELETE FROM userTable").rowcount
conn.execute("DELETE FROM partyTable").rowcount
c.execute("CREATE TABLE IF NOT EXISTS userTable \
    (name text PRIMARY KEY, itameLevel inteager, job text, origin inteager)")

c.execute("CREATE TABLE IF NOT EXISTS partyTable \
   (name text PRIMARY KEY, orehaNomal inteager, orehaHard inteager, argos1 inteager, argos2 inteager, argos3 inteager, baltanNomal inteager, viakissNomal inteager, baltanHard inteager, viakissHard inteager)")

total = main()
# with open('partylist.csv', 'w', encoding='utf-8-sig', newline='') as file:
#     write = csv.writer(file)
#     write.writerows(total)
for i in total:
    data = "INSERT INTO userTable \
VALUES('"+i[0]+"',"+ str(i[1])+",'"+i[2]+"',"+str(i[3]) +")"
    c.execute(data)
    partyData = "INSERT INTO partyTable \
VALUES('"+i[0]+"',0,0,0,0,0,0,0,0,0)"
    c.execute(partyData)