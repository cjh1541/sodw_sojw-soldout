from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd

import mDriver_mode as mDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from pymongo import MongoClient, UpdateOne
from datetime import datetime

    
# 엑셀 불러와서 가격,품절여부 확인
def 동원몰품절확인():
    print("동원몰 품절확인 시작")
    # 엑셀불러오기
    # df_dw = pd.read_excel('./진행상품/테스트용진행상품.xls',sheet_name='동원몰')
    
    # print(df_dw['상품명'])
    
    L_Code = []
    #관리코드 숫자만 남기기
    for maincode in L_dwCode:
        code = maincode[4:]
        L_Code.append(code)
    
    operations = []
    #동원몰 긁어오기
    for code,maincode in zip(L_Code,L_dwCode[:]):
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
        # element = tree.xpath("//em[@class='userPriceText']")[0].text
        # print(element)
        
        # 품절 요소 찾기
        try:
            elements = tree.xpath("//button[@class='btn_lg btn_soldout_lg']")
            if len(elements) >0:
                print("품절임")
                element = tree.xpath("//button[@class='btn_lg btn_soldout_lg']")[0].text
                # print(element)
                status = "품절"
            else:
                print("품절아님")
                element = tree.xpath("//button[@class='btn_lg btn_buy_lg']")[0].text
                # print(element)
                status = "판매중"
            print(f'코드:{maincode} , {status}')
        except:
            status = "에러"
            print(f'코드:{maincode} , {status}')
            
        # db 업로드
        # # db 업로드
        update_DB(maincode,status)
        # operations.clear
        # operations.append(
        #     UpdateOne(
        #     {"판매자관리코드": code},
        #     {"$set": {"사이트상태": status,"작업날짜":formatted_date}},
        #     upsert=True  # 존재하지 않는 경우 새 문서로 삽입
        #     )
        # )
        # result = collection.bulk_write(operations)
    
        
def 정원몰품절확인():
    print("정원몰 품절확인 시작")
    # 엑셀불러오기
    # df_jw = pd.read_excel('./진행상품/테스트용진행상품.xls',sheet_name='정원몰')
    
    # print(df_jw['상품명'])
    
    L_Code = []
    #관리코드 숫자만 남기기
    for maincode in L_jwCode:
        code = maincode[4:]
        L_Code.append(code)
        
    global driver
    driver = mDriver.make_driver('t2',mode='pc')
        
    operations = []
    #정원몰 긁어오기
    for code,maincode in zip(L_Code,L_jwCode):
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
            print(f'코드:{maincode} = 품절입니다.')
            status = "품절"
            
            # # db 업로드
            update_DB(maincode,status)
        
            continue
        except NoAlertPresentException:
            # print("Alert 창이 없습니다.")
            pass
        
        
        # 품절 구매 요소 있는지 확인
        try:
            # 품절일때
            # selector = "//div[@class='btn_choice_box btn_restock_box']//button[@class='btn_add_soldout']"
            selector = "//button[@class='btn_add_soldout']"
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
            element = driver.find_element(By.XPATH, selector)
            print(f'코드:{code} , {element.text}')
            status = "품절"

        except:
            try:
                # 구매 가능 요소 있을때
                selector = "//button[@class='btn_add_order']" 
                WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, selector)))  # 검색결과 기다리기
                element = driver.find_element(By.XPATH, selector)
                print(f'코드:{code} , {element.text}')
                status = "판매중"
            except:
                status = "에러"
        
        # # db 업로드
        update_DB(maincode,status)
        # operations.clear
        # operations.append(
        #     UpdateOne(
        #     {"판매자관리코드": code},
        #     {"$set": {"사이트상태": status,"작업날짜":formatted_date}},
        #     upsert=True  # 존재하지 않는 경우 새 문서로 삽입
        #     )
        # )
        # result = collection.bulk_write(operations)
        
# db업로드 
def update_DB(code,status):
    
    operations = []
    operations.append(
        UpdateOne(
        {"판매자관리코드": code},
        {"$set": {"사이트상태": status,"작업날짜":formatted_date}},
        upsert=True  # 존재하지 않는 경우 새 문서로 삽입
        )
    )
    result = collection.bulk_write(operations)
        
# db 엑셀로 저장하기
def save_excel():

    # MongoDB에서 데이터 가져오기
    data = list(collection.find({}, {'_id': 0}))

    # DataFrame으로 변환
    df = pd.DataFrame(data)

    # 엑셀 파일로 저장
    df.to_excel("output.xlsx", index=False, engine='openpyxl', encoding='utf-8-sig')
    print(f'save Excel : output.xlsx')
            
def db_init():
    global collection, L_dwCode, L_jwCode,formatted_date
    L_dwCode = []
    L_jwCode = []
    
    # 오늘 날짜 가져오기
    today = datetime.today()

    # 오늘 날짜를 'YY/MM/DD' 형식으로 출력
    formatted_date = today.strftime('%y/%m/%d')
    
    # db 연결
    client = MongoClient("mongodb+srv://richases:1200djrdnjs%40@mart.2nnalxu.mongodb.net/")   
    db = client.soldout_check
    
    # collection = db.test_soldout # 테스트용
    collection = db.soldout_chk # 정상용
    
    # MongoDB에서 '판매자관리코드' 컬럼의 값만 가져오기
    data = collection.find({}, {'판매자관리코드': 1, '_id': 0})
    
    # '판매자관리코드' 값만 추출하여 리스트로 저장
    data = [item['판매자관리코드'] for item in data]
    
    # 동원몰 정원몰 코드 구분하기
    for codes in data[:]:

        #정원몰
        if codes[:4] == "sojw" or codes[:4] == "SOJW":
           L_jwCode.append(codes)
        #동원몰
        elif codes[:4] == "sodw" or codes[:4] == "SODW":
           L_dwCode.append(codes)
        else:
           print(f'대소문자 구분하기 : {codes}')
           pass
    
    print("DB_init() 완료")        

    
def main():
    # db 연결 및 코드 추출
    db_init()
    동원몰품절확인()
    정원몰품절확인()
    save_excel()
    
if __name__ == "__main__":
    # test()
    # 정원몰품절확인()
    main()