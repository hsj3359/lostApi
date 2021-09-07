from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.parse
import sqlite3

total = list()
def main():
    name = ["메난민받아주세요", "에플릿", "미래의미중년", "쓸데없이멋있는모코코", "12글자나되니까꽉채웠음", "발헤임할꺼에요", "아리아나그렇죠", "아이스바닐라커피"]

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
                total.append(data)



conn = sqlite3.connect("lostParty.db", isolation_level=None)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS userTable \
    (name text PRIMARY KEY, itameLevel inteager, job text, origin inteager)")

main()
for i in total:
    data = "INSERT INTO userTable \
VALUES('"+i[0]+"',"+ str(i[1])+",'"+i[2]+"',"+str(i[3]) +")"
    c.execute(data)