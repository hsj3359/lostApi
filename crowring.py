import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib.parse
import sqlite3


def main():
    tampTotal = list()
    html = urlopen("https://blog.naver.com/dbsgml9693/222535475471")
    bsObject = BeautifulSoup(html, "html.parser")
    nickName = bsObject.select('body')
    print(nickName)



main()

