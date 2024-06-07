from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd

import mDriver_mode as mDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


def test():
    global driver
    driver = mDriver.make_driver('t2',mode='pc')
    url = "https://www.jungoneshop.com/goods/goods_view.php?goodsNo=6035"
    
    driver.get(url)
    
    # 품절일때
    selector = "//div[@class='btn_choice_box btn_restock_box']//button[@class='btn_add_soldout']"
    WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
    element = driver.find_element(By.XPATH, selector)
    print(f'코드:6035 , {element.text}')

    
# 엑셀 불러와서 가격,품절여부 확인
def 동원몰품절확인():
    # 엑셀불러오기
    df_dw = pd.read_excel('./진행상품/테스트용진행상품.xls',sheet_name='동원몰')
    
    print(df_dw['상품명'])
    
    L_dwCode = []
    #관리코드 숫자만 남기기
    for maincode in df_dw['판매자관리코드']:
        code = maincode[4:]
        L_dwCode.append(code)
        
    #동원몰 긁어오기
    for code in L_dwCode:
        base_url = "https://www.dongwonmall.com/product/detail.do?productId="
        url = base_url + code
        
        response = requests.get(url)
        response.raise_for_status()
        
        # soup = BeautifulSoup (page.content, "html.parser") #기존
        # BeautifulSoup로 HTML 파싱
        soup = BeautifulSoup(response.content, 'lxml') #gpt code
        
        # XPath를 BeautifulSoup에서 사용 가능한 형식으로 변환
    # BeautifulSoup은 XPath를 직접 지원하지 않으므로 lxml의 etree를 사용

        parser = etree.HTMLParser()
        tree = etree.fromstring(str(soup), parser)
        
        # dom = etree.HTML (str(soup))
        element = tree.xpath("//em[@class='userPriceText']")[0].text
        print(element)
        
        # 품절 요소 찾기
        elements = tree.xpath("//button[@class='btn_lg btn_soldout_lg']")
        if len(elements) >0:
            print("품절임")
            element = tree.xpath("//button[@class='btn_lg btn_soldout_lg']")[0].text
            print(element)
        else:
            print("품절아님")
            element = tree.xpath("//button[@class='btn_lg btn_buy_lg']")[0].text
            print(element)
        
def 정원몰품절확인():
    # 엑셀불러오기
    df_jw = pd.read_excel('./진행상품/테스트용진행상품.xls',sheet_name='정원몰')
    
    print(df_jw['상품명'])
    
    L_dwCode = []
    #관리코드 숫자만 남기기
    for maincode in df_jw['판매자관리코드']:
        code = maincode[4:]
        L_dwCode.append(code)
        
    global driver
    driver = mDriver.make_driver('t2',mode='pc')
        
    #정원몰 긁어오기
    for code in L_dwCode:
        base_url = "https://www.jungoneshop.com/goods/goods_view.php?goodsNo="
        url = base_url + code
        # print(f'코드 = {code}')
        
        driver.get(url)
        
        # 팝업창 대기 및 닫기 (옵션)
        try:
            # Alert 창으로 전환
            alert = driver.switch_to.alert
            # Alert 창의 텍스트 출력 (선택 사항)
            print(alert.text)
            # Alert 창 확인 버튼 클릭
            alert.accept()
            print(f'코드:{code} = 품절입니다.')
            continue
        except NoAlertPresentException:
            # print("Alert 창이 없습니다.")
            pass
        
        # # 가격 가져오기
        # selector = "//strong[@class='option_price_display_0']"
        # WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
        # element = driver.find_element(By.XPATH, selector)
        # print(element.text)
        
        # 품절 구매 요소 있는지 확인
        try:
            # 품절일때
            # selector = "//div[@class='btn_choice_box btn_restock_box']//button[@class='btn_add_soldout']"
            selector = "//button[@class='btn_add_soldout']"
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
            element = driver.find_element(By.XPATH, selector)
            print(f'코드:{code} , {element.text}')

        except:
            # 구매 가능 요소 있을때
            selector = "//button[@class='btn_add_order']" 
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
            element = driver.find_element(By.XPATH, selector)
            print(f'코드:{code} , {element.text}')
            

    
if __name__ == "__main__":
    # test()
    정원몰품절확인()