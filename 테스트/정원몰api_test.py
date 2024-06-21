from bs4 import BeautifulSoup
from lxml import etree
import requests
import os,sys
import pandas as pd

# from 테스트 import mDriver_mode_test as mDriver
import mDriver_mode_test as mDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


    
# 정원몰 bs4 로 크롤링 가능(확인함)
def test2():
    # 정원몰 bs4 로 크롤링 가능(확인함)
    url = "https://search.shopping.naver.com/search/all?query=%EC%A4%84%EB%88%88"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'lxml')
    
    # print(f'soup : {soup}')

    # # HTML 데이터를 보기 좋게 포맷팅
    # formatted_html = soup.prettify()

    # # txt 파일로 저장
    # with open('정원몰bs4 테스트.txt', 'w', encoding='utf-8') as file:
    #     file.write(formatted_html)
        
    parser = etree.HTMLParser()
    tree = etree.fromstring(str(soup), parser)
    
    # dom = etree.HTML (str(soup))
    element = tree.xpath("//button[@class='btn_add_order']")[0].text
    print(f'element : {element}')
        
'''
api 로 크롤링 하기 테스트  (밑에부터)
'''
        
def test():
    global driver
    driver = mDriver.make_driver('t1',mode='pc')
    
    url = "https://search.shopping.naver.com/search/all?query=%EC%A4%84%EB%88%88"
    driver.get(url)
    
    # url = "https://sleepy-it.tistory.com/6"
    url = "https://search.shopping.naver.com/search/all?query=%EC%A4%84%EB%88%88"
    # url = "https://search.shopping.naver.com/api/search/all?adQuery=%EC%A4%84%EB%88%88&eq=&iq=&origQuery=%EC%A4%84%EB%88%88&pagingIndex=1&pagingSize=40&productSet=model&query=%EC%A4%84%EB%88%88&sort=rel&viewType=list&window=&xq="
    driver.get(url)
    
    
    # selector = "//button[@class='btn_add_order']" 
    # WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
    # element = driver.find_element(By.XPATH, selector)
    # print(f'element : {element.text}')
    input()
    
def test3():
    keyword = "줄눈"
    url  = f"https://search.shopping.naver.com/search/all?query={keyword}"
    url = "https://search.shopping.naver.com/api/search/all?adQuery=%EC%A4%84%EB%88%88&eq=&iq=&origQuery=%EC%A4%84%EB%88%88&pagingIndex=1&pagingSize=40&productSet=model&query=%EC%A4%84%EB%88%88&sort=rel&viewType=list&window=&xq="

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

    res = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(res.content, 'lxml')

    print(soup)
    
    
def load_excel():
    # path = './output.xlsx'
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 상위 부모 디렉토리 경로
    parent_dir = os.path.dirname(current_dir)
    print(parent_dir)
    
    path = parent_dir + "\작업용 엑셀\초기 db 업로드용.csv"

    print(path)

    df = pd.read_csv(path)
    print(df) 
    print(df['판매자관리코드'])
    
    test_code = [
        "SOJW3353","SOJW2497","SOJW603","SOJW3252","SOJW3244",
        "SOJW2487","SOJW601","SODW001462805","SOJW24313"
    ]
    
    L_code = []
    for code in test_code:
        L_code.append(code[4:])
    
    print(L_code)
    
    print(L_code)
    
    driver = mDriver.make_driver('t2',mode='pc')
    
    for code in L_code:
        url = "https://www.jungoneshop.com/goods/goods_view.php?goodsNo="
        allUrl = url + code
        driver.get(allUrl)
        
        try:
            selector = "//button[@class='btn_add_order']" 
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
            element = driver.find_element(By.XPATH, selector)
            print(f'element : {element.text}')
        except Exception as error:
            print(f'에러코드:{code}')
            print(error)
            

if __name__ == "__main__":
    test3()
    # load_excel()