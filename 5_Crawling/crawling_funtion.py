def get_links():
    '''
    잡코리아 공고 링크 및 기업이름 가져오는 함수
    parms= ''
    return= 공고 링크 및 기업 이름 리스트
    '''
    num=1
    link_list=[]   
    cor_title_list=[]
    while num<=25:
        url= urlopen(f'https://www.jobkorea.co.kr/Search/?stext=python&tabType=recruit&Page_No={num}')
        soup= BeautifulSoup(url, 'html.parser')

        links= soup.find_all('a', {'class': "corp-name-link dev-view"})
        for link in links:
            link= link['href']
            link_list.append(link)
            print(link)
        for link in links:
            link= link.text.strip()
            cor_title_list.append(link)
            print(link)
        num+=1
        time.sleep(2)
    return link_list, cor_title_list

def get_skill(recuit_link_list):
    '''
    채용공고의 스킬 및 기업정보 링크를 가져오는 함수
    params= 기업공고 링크 링스트
    return= 채용공고의 스킬 및 기업정보 링크 리스트
    '''
    other_lang_list, cor_link_list= [], []
    for link in recuit_link_list:
        url= urlopen(f'https://www.jobkorea.co.kr{link}')
        soup= BeautifulSoup(url, 'html.parser')

        # 스킬 추출
        try:
            jar1=soup.find('dt', text='스킬').next.next.next.text.strip().split(',')
            loc_list= list(jar1)
            print(jar1)
            for loc in (loc_list):
                print(loc.strip())
                other_lang= loc_list       
                other_lang_list.append(loc.strip())

        except Exception as e:
        
            print(e)
        time.sleep(4)
        #링크 추출
        cor_links= soup.find('a', {'class': 'girBtn girBtn_3'})    #링크 데이터 추출
        jar=cor_links['href']
        cor_link_list.append(jar)
    return other_lang_list, cor_link_list

def get_salary_links(cor_link_list):
    '''
    기업정보 링크 통해서 연봉정보 링크 가져오는 함수
    parmas=기업 정보 링크 리스트
    return= 연봉정보 링크 리스트
    
    '''
    salary_link_lists=[]
    for link in cor_link_list:
        url= urlopen(f'https://www.jobkorea.co.kr{link}')
        soup= BeautifulSoup(url, 'html.parser')
        try:
            jar= soup.find_all('a', {'class': "company-nav-item" })[2] if soup.find_all('a', {'class': "company-nav-item" })[2] else 'null'
            jar2= jar['href']
        except Exception as e:
            print(e)
        salary_link_lists.append(jar2)
        time.sleep(4)
    return salary_link_lists


def get_salary_info(salary_link_lists):
    '''
    전체 평균 연봉을 가져오는 함수
    params= 연봉정보 링크 리스트
    return= 연봉정보 리스트
    '''
    salary_lists=[]
    for link in salary_link_lists:
            url= urlopen(f'https://www.jobkorea.co.kr{link}')
            soup= BeautifulSoup(url, 'html.parser')
            try:
                jar= soup.find('div', {'class': 'salary'}).text.strip()
                jar2= jar.replace('만원', '') if jar else 'null'
                jar3= jar2.replace('\n', '') if jar2 else 'null'
                salary_lists.append(jar3)
            except Exception as e:
                print(e)
    time.sleep(4)

def get_loc(recuit_link_list):
    """
    구인지역을 가져오는 함수
    params= 기업공고 링크 리스트
    return= 기업공고의 근무지역 리스트
    """
    loc_lists=[]
    for link in recuit_link_list:
        url= urlopen(f'https://www.jobkorea.co.kr{link}')
        soup= BeautifulSoup(url, 'html.parser')
        dl_tags = soup.find_all('dl', {'class': "tbList"}) #tblist 클래스 가져오기
        for dl in dl_tags:
                dt_tag = dl.find('dt', text='지역')   # '지역' 정보가 있는 <dt> 태그 찾기
                if dt_tag:
                    dd_tag = dt_tag.find_next_sibling('dd') #dd 테그찾기
                    if dd_tag:
                        location_links = dd_tag.find_all('a') # a 테그찾기
                        for link in location_links:
                            loc_lists.append(link.text)
                            print(link.text)
        time.sleep(4)
    return loc_lists 