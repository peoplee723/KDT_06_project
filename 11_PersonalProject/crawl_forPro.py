import os
import sys
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter
# from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from urllib.parse import quote


# 질문
# div.questionDetail
# 대답
# answer_1 > div.answerDetail._endContents._endContentsText




def get_links(time_list, query, title):
    '''
    뉴스 링크 가져오는 함수
    return
    '''
    article_link_list=[]
    for time in time_list:
        url= urlopen(f'https://kin.naver.com/search/list.naver?query={query}&page={time}')
        soup= BeautifulSoup(url, 'html.parser')

        # jar2= soup.find_all('a',{'class':"_nclicks:kin.txt _searchListTitleAnchor"})
        jar2=soup.find_all('dt')
        for j in jar2:
            # print(j)
            # print(j.find('img', {'class':'ico_pro'}))
            if j.find('img', {'class':'ico_pro'}):
        #         print(j.get('alt'))
                link= j.find('a')['href']
                article_link_list.append(link)
            # print(link)
        if time%100==0:
            print(time)
    # 데이터 프레임으로 저장
    linkDF=pd.DataFrame()
    linkDF['link']=article_link_list
    linkDF.to_csv('./link_'+title+'.csv')
    print(len(article_link_list))

    return article_link_list
# 크롤링 범위 지정 (page)
time_list=[]
for a in range(1,1000):
    time_list.append(a)

# 자녀장려세제 : 너무 적어...
# 부가가치세: %EB%B6%80%EA%B0%80%EA%B0%80%EC%B9%98%EC%84%B8
# 상속세: %EC%83%81%EC%86%8D%EC%84%B8
# 종합소득세: %EC%A2%85%ED%95%A9%EC%86%8C%EB%93%9D%EC%84%B8
# 연말정산: %EC%97%B0%EB%A7%90%EC%A0%95%EC%82%B0
# 양도소득세: %EC%96%91%EB%8F%84%EC%86%8C%EB%93%9D%EC%84%B8
# 국제조세: %EA%B5%AD%EC%A0%9C%EC%A1%B0%EC%84%B8
# 종합부동산세: %EC%A2%85%ED%95%A9%EB%B6%80%EB%8F%99%EC%82%B0%EC%84%B8
# 근로장려세제: 
# 법인세: %EB%B2%95%EC%9D%B8%EC%84%B8
# 국세기본징수법: 
# 국세기본(법): %EA%B5%AD%EC%84%B8%EA%B8%B0%EB%B3%B8
# 국세징수법: %EA%B5%AD%EC%84%B8%EC%A7%95%EC%88%98
# 기타세목
# 링크 크롤링
query='%EA%B5%AD%EC%84%B8%EC%A7%95%EC%88%98'

title='국세징수'
# get_links(time_list, query, title)

# ++ 추가 크롤링 사이트: 찾아줘 세무사 (무료 Q&A)
# https://findsemusa.com/search/searchconsult.do?page=1&sord=OA&skey=&stype=10&cateno=10#


def get_QNA(links, path, title):
    a_list, q_list=[],[]
    count=1
    for i in links:
        link=i
        encoded_link = quote(link, safe=':/?=&')
        request = urllib.request.Request(encoded_link)
        url= urlopen(request)
        response= url.read().decode('utf-8')
        soup= BeautifulSoup(response, 'html.parser')


        # 질문 추출
        jar2= soup.find('div',{'class':"questionDetail"})
        # print(jar2.get_text(strip=True), type(jar2))
        q= (jar2.get_text(strip=True))
        # print(q)
        q_list.append(q)
        # 대답 추출
        # jar3= soup.find_all('div', {'class': 'se-main-container'})
        jar3=soup.find_all('div', {'class': "answerDetail _endContents _endContentsText"})
        # print(jar3[0].get_text(), len(jar3))
        a=[]
        for j in range(len(jar3)):
            text=jar3[j].get_text(strip=True)
            a.append(text.replace('\u200b', ''))
            # print(text)
        # 추출한 텍스트 리스트에 추가
        a_list.append(a)
        # print(a_list, len(a_list))
        if count%100==0: print(count)
        count+=1
    # 크롤링한 데이터 DF로 저장
    qnaDF=pd.DataFrame()
    qnaDF['question']=q_list
    qnaDF['answer']=a_list
    qnaDF.to_csv(path+title, index=False)

    return qnaDF

def get_pro_qna(links, path, title):
    a_list, q_list=[],[]
    count=1
    try:
        for i in links:
            link=i
            encoded_link = quote(link, safe=':/?=&')
            request = urllib.request.Request(encoded_link)
            url= urlopen(request)
            response= url.read().decode('utf-8')
            soup= BeautifulSoup(response, 'html.parser')

            # 질문 추출
            jar2= soup.find('div',{'class':"questionDetail"})
            q= (jar2.get_text(strip=True))

            # 대답 추출
            a_box=[]
            a=soup.find_all('div',  
                        {'class': "answerDetail _endContents _endContentsText"})
            for i  in a:
                a_box.append(i.get_text(strip=True))
            if not jar3: 
                jar3=soup.find('div', {'class':"_contentBox contentBox contentBox--headerAnswerContent"})
                if jar3:
                    a_box=jar3.find('div', {'class': "answerDetail _endContents _endContentsText"}).get_text(strip=True)
            else:
                for j in jar3:
                    j2= j.find('div', {'class':"profile_info"})
                    # 전문가 답변인지 구분
                    jar5=j2.find('span', {'class':"badge expert_job"})
                    if jar5:
                        a=j.find('div',  
                                    {'class': "answerDetail _endContents _endContentsText"}).get_text(strip=True)
                        a_box.append(a.replace('\u200b', ''))
            
        # 답변이 여러개일 경우 따로 저장
            for i in range(len(a_box)):
                q_list.append(q)
                a_list.append(a_box[i])
        # 디버깅
            if count%100==0: print(count)
            count+=1
            # print(q, a_box, len(a_box))
    except Exception as e:
        print(e)
        # 하나의 데이터프레임에 저장
    qnaDF=pd.DataFrame()
    qnaDF['question']=q_list
    qnaDF['answer']=a_list
    qnaDF.to_csv(path+title, index=False)
    return q_list, a_list

# get_pro_qna([test_link])

# 질문과 대답 크롤링 

DEAULT_PATH='./data/'
linklist=os.listdir(DEAULT_PATH)[:10]
for link in linklist:
    linkDF=pd.read_csv(DEAULT_PATH+link)['link']
    newtitle=link.replace('link', 'QNA')
    
    q_list, a_list=get_pro_qna(linkDF, DEAULT_PATH, newtitle)