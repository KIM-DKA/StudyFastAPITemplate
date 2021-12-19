# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os 
import pandas as pd 
import openpyxl
import time 
import numpy as np 



# 검색 날짜 지정 
st = [x.strftime('%Y%m%d') for x in pd.date_range('20200101','20200201',freq='2D')]
fns = [x.strftime('%Y%m%d') for x in pd.date_range('20200102','20200201',freq='2D')]

t = abs(np.random.normal(0,1,len(st)))




# 크롬 드라이버로 크롬을 실행한다.
os.chdir('C:\\Users\\rlaem\\Desktop\\craw')
results = []
driver = webdriver.Chrome('./chromedriver')


for s,f in zip(st,fns):

    # 입찰정보 검색 페이지로 이동
    driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do')

    # 업무 종류 체크 전체면 무시) 
    task_dict = {'전체': 'taskClCds'}

    for task in task_dict.values():
        if task == 'taskClCds': 
            continue
        checkbox = driver.find_element_by_id(task)
        checkbox.click()
    
    # 검색어
    query = '빅데이터'
    # id값이 bidNm인 태그 가져오기
    bidNm = driver.find_element_by_id('bidNm')
    # 내용을 삭제 (버릇처럼 사용할 것!)
    bidNm.clear()
    # 검색어 입력후 엔터
    bidNm.send_keys(query)
    bidNm.send_keys(Keys.RETURN)

    # 검색 조건 체크
    #option_dict = {'검색시작일': 'setMonth1_1', '입찰마감건 제외': 'exceptEnd', '검색건수 표시': 'useTotalCount'}
    #option_dict = {'검색시작일': 'fromBidDt', '검색마감일' : 'toBidDt'}

    """ for option in option_dict.values():
        checkbox = driver.find_element_by_id(option)
        checkbox.click()
    """ 

    # 시작 날짜 

    search_box = driver.find_element_by_xpath('//*[@id="fromBidDt"]')
    search_box.clear()
    search_box.send_keys(s)

    # 종료 날짜  

    search_box = driver.find_element_by_xpath('//*[@id="toBidDt"]')
    search_box.clear()
    search_box.send_keys(f)

    # 목록수 100건 선택 (드롭다운)
    #recordcountperpage = driver.find_element_by_name('recordCountPerPage')
    #selector = Select(recordcountperpage)
    #selector.select_by_value('100')

    # 검색 버튼 클릭
    search_button = driver.find_element_by_class_name('btn_mdl')
    search_button.click()

    # 검색 결과 확인
    elem = driver.find_element_by_class_name('results')
    div_list = elem.find_elements_by_tag_name('div')
 

    


    # 검색 결과 모두 긁어서 리스트로 저장
    
    for div in div_list:
        results.append(div.text)
        a_tags = div.find_elements_by_tag_name('a')
        if a_tags:
            for a_tag in a_tags:
                link = a_tag.get_attribute('href')
                if len(link) == 0:
                    pass 
                else : 
                    results.append(link)
                    time.sleep(0.5)
                    print('{st} 진행 했으며 0.5초후 다시실행'.format(st=s))
    




# 검색결과 모음 리스트를 12개씩 분할하여 새로운 리스트로 저장 

result = [results[i * 12:(i + 1) * 12] for i in range((len(results) + 12 - 1) // 12 )]


url_list = [x[2] for x in result]
category = [x[0] for x in result]



#######################################################################################

driver = webdriver.Chrome('./chromedriver')

# url list 받아오기 

#######################################################################################

data = {'업무':[],'입찰공고번호':[],'차수':[],'공고명':[],'수요기관명':[],'입찰개시':[],'입찰마감':[],'배정예산':[]}

driver = webdriver.Chrome('./chromedriver')

for i in range(len(url_list)):

    driver.get(url_list[i])

    # 버튼 제거         
    search_button = driver.find_element_xpath('//*[@id="epDialogBtns"]/a/span')

    driver.execute_script("arguments[0].click();",search_button)

    # 업무 
    data['업무'].append(category[i])

    # 입찰공고 번호

    //*[@id="container"]/div[6]/table/tbody/tr[2]/td[1]/div
    no = driver.find_element_by_xpath('//*[@id="container"]/div[5]/table/tbody/tr[2]/td[1]/div').text
    data['입찰공고번호'].append(no.split('-')[0].strip()) 
    

    # 차수 
    
    data['차수'].append(no.split('-')[1])

    # 공고명
    title = driver.find_element_by_xpath('//*[@id="container"]/div[5]/table/tbody/tr[3]/td/div').text
    data['공고명'].append(title.split('\n')[0])


    # 수요기관명 
    data['수요기관명'].append(driver.find_element_by_xpath('//*[@id="container"]/div[5]/table/tbody/tr[4]/td[1]/div/span').text) 

    # 입찰개시 
    data['입찰개시'].append(driver.find_element_by_xpath('//*[@id="container"]/div[7]/table/tbody/tr[1]/td[1]/div').text[0:10])

    # 입찰마감일 
    data['입찰마감'].append(driver.find_element_by_xpath('//*[@id="container"]/div[7]/table/tbody/tr[1]/td[2]/div').text[0:10])

    # 배정예산 

    data['배정예산'].append(driver.find_element_by_xpath('//*[@id="container"]/div[9]/table/tbody/tr[2]/td[1]/div').text[:-1])

    time.sleep(0.5)

    print('{i} 번째 진행중 {n} 개 남음'.format(i=i,n=len(url_list)-i))