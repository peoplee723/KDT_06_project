from bs4 import BeautifulSoup
from urllib.request import urlopen 
from selenium import webdriver
import requests
import time
import pandas as pd


pd.Timestamp(19503+150, unit="D").strftime("%Y%m%d")

url=f'https://news.naver.com/breakingnews/section/102/250?date=20240101'
html=requests.get(url)
soup=BeautifulSoup(html.text,'html.parser')
ly=soup.find('div',{'class':'sa_text'}).find_all('a')
for news in ly:
    link=news.get('href')
    # 링크
    print(link)

    driver=webdriver.Chrome()

    driver.get(link)
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    a=soup.find('article')
    print(a)
    time.sleep(3)