from pymongo import MongoClient, UpdateOne
import pandas as pd
from datetime import datetime


def connect():
    global client,db
    client = MongoClient("mongodb+srv://richases:1200djrdnjs%40@mart.2nnalxu.mongodb.net/")
    
    db = client.test_mart

def test():
    connect()
    collection = db.test
    
    df_dw = pd.read_excel('./진행상품/테스트용진행상품.xls',sheet_name='동원몰')
    # 오늘 날짜 가져오기
    today = datetime.today()

    # 오늘 날짜를 'YY/MM/DD' 형식으로 출력
    formatted_date = today.strftime('%y/%m/%d')
    
    number = len(df_dw.index)
    
    operations= []
    for data in range(0,number):
        operations.clear
        code = df_dw['판매자관리코드'][data]
        prd = df_dw['상품명'][data]
        price = df_dw['판매가'][data]
        nowSell = df_dw['수집사이트'][data]
        chkSell = "판매중"
        date = formatted_date
    
        dic_oneChk ={
            '코드':code, '상품명':prd, '현재가격':price, '현재상태':nowSell, '사이트상태':chkSell,'작업날짜':date
        }
        operations.append(
            UpdateOne(
            {"판매자관리코드": code},
            {"$set": {"사이트상태": chkSell,"작업날짜":date}},
            upsert=True  # 존재하지 않는 경우 새 문서로 삽입
            )
        )
        result = collection.bulk_write(operations)
        print(f"삽입된 문서 수: {result.upserted_count}")
        print(f"업데이트된 문서 수: {result.modified_count}")
        
        save_excel(collection)
        
def save_excel(collection):


    # MongoDB에서 데이터 가져오기
    data = list(collection.find({}, {'_id': 0}))

    # DataFrame으로 변환
    df = pd.DataFrame(data)

    # 엑셀 파일로 저장
    df.to_excel("output.xlsx", index=False, engine='openpyxl', encoding='utf-8-sig')
    
#db 에서 코드불러오기
def load_code():
    client = MongoClient("mongodb+srv://richases:1200djrdnjs%40@mart.2nnalxu.mongodb.net/")
    
    db = client.soldout_check
    collection = db.soldout_chk
    
    # MongoDB에서 '판매자관리코드' 컬럼의 값만 가져오기
    data = collection.find({}, {'판매자관리코드': 1, '_id': 0})
    
    # '판매자관리코드' 값만 추출하여 리스트로 저장
    data = [item['판매자관리코드'] for item in data]
    print(data)
    
    
if __name__ == "__main__":
    load_code()