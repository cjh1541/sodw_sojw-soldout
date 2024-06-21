# import mDriver_mode as mDriver
from selenium.webdriver.common.by import By
import requests,re
from bs4 import BeautifulSoup
import json


    
def test():

    url = "https://search.shopping.naver.com/api/search/all?adQuery=%EC%A4%84%EB%88%88&eq=&iq=&origQuery=%EC%A4%84%EB%88%88&pagingIndex=1&pagingSize=40&productSet=model&query=%EC%A4%84%EB%88%88&sort=rel&viewType=list&window=&xq="
    html = requests.get(url)
    soup = BeautifulSoup(html.content,'lxml')
    print(str(soup))
    
    # soup = BeautifulSoup(response.content, 'lxml')
    
    # # # txt 파일로 저장
    # with open('정원몰bs4 테스트.txt', 'w', encoding='utf-8') as file:
    #     file.write(soup)
    
    
def test2():
    cookies = {
    'NNB': 'LTJAQAJDQJAF6',
    'ASID': '7095fe91000001743cdb06db0000004f',
    'NV_WETR_LOCATION_RGN_M': '"MDIyODExMjg="',
    'NDARK': 'Y',
    'recent_card_list': '2615,2488,2345,1716,223,1530,3637',
    '_ga': 'GA1.1.86063451.1608575479',
    '_ga_3X9JZ731KT': 'GS1.1.1691224416.2.0.1691224416.0.0.0',
    '_fwb': '65z17VnF7mt0agYZ7UgboR.1705494694157',
    'SHP_BUCKET_ID': '1',
    'NID_AUT': 'y0f4KqLTTSCDv1ifsyzl/UDdocd83J6seuIDvNAj9dHPrApybI3dohybmFrzl+Gh',
    'NID_JKL': '+ifIQpowtwArdDHx+5XrNrAMdh+6xKYi5Bq21W9hJIc=',
    'NFS': '2',
    'NV_WETR_LAST_ACCESS_RGN_M': '"MDIyODExMjg="',
    'NAC': 'LHpOBMQJn2Ao',
    'NACT': '1',
    'spage_uid': '',
    'NID_SES': 'AAABwx/GLl9mrvLA8Llw9wERKRhifhhqD58gmyI3XN5QEdQk1p5Wd/TMgEV5zyZdM7iJH1rb1BVmUMjzIEkuhnrCrzpYquB/F63qizZZByTIopFSDeo464IbfID7BeldvuNpD8wga519R1dMMEAVSu5630nFgrwlgdKmKGy/boqf4e9a2zoEXQ41czfjntx4ojVrj8dt4w8tRDbKjW0nOR66j/SoRsSM0oKositxggGo3kqnq7XEsx4at8fvhUL0f7ZW5shyX0djcvD3+lfvKJmM1Zf7XqvSN4+tFpQ+snNVexXo/7VYgphjoXb/wvb/geAeXjV5MKf43Dh5A8gpbkktTzFGGh9R4Sq/FkEW57oBKemWSuh9kFlEHs7aqhstdwx20ry/oPi/Kb1Vd7INYmgIqlbn/AGqVE+zhUhMuDV6VcSjpC11lA+SS4VxflnigXz8vM1awUfHtiU0RMZ5fAaZ18clZfNFlTIOgSLincaQP4IaxPa2x4HySHaP+v4vM2jdxy9BODI2pn69B0VsMNkxrDAUSDfVVahcuxFd0RBInJfgOaFseqS1g/aydRF10PlWSjT6FUqA1Mql3rjz7VSZDyb/3Hn5BK4Nz9JzS1DxDNlb',
    'BUC': 'Fge8ShcXw_mMccnewRPXBdaQ1HWsknjVath0ljJMdK4=',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6',
        # 'cookie': 'NNB=LTJAQAJDQJAF6; ASID=7095fe91000001743cdb06db0000004f; NV_WETR_LOCATION_RGN_M="MDIyODExMjg="; NDARK=Y; recent_card_list=2615,2488,2345,1716,223,1530,3637; _ga=GA1.1.86063451.1608575479; _ga_3X9JZ731KT=GS1.1.1691224416.2.0.1691224416.0.0.0; _fwb=65z17VnF7mt0agYZ7UgboR.1705494694157; SHP_BUCKET_ID=1; NID_AUT=y0f4KqLTTSCDv1ifsyzl/UDdocd83J6seuIDvNAj9dHPrApybI3dohybmFrzl+Gh; NID_JKL=+ifIQpowtwArdDHx+5XrNrAMdh+6xKYi5Bq21W9hJIc=; NFS=2; NV_WETR_LAST_ACCESS_RGN_M="MDIyODExMjg="; NAC=LHpOBMQJn2Ao; NACT=1; spage_uid=; NID_SES=AAABwx/GLl9mrvLA8Llw9wERKRhifhhqD58gmyI3XN5QEdQk1p5Wd/TMgEV5zyZdM7iJH1rb1BVmUMjzIEkuhnrCrzpYquB/F63qizZZByTIopFSDeo464IbfID7BeldvuNpD8wga519R1dMMEAVSu5630nFgrwlgdKmKGy/boqf4e9a2zoEXQ41czfjntx4ojVrj8dt4w8tRDbKjW0nOR66j/SoRsSM0oKositxggGo3kqnq7XEsx4at8fvhUL0f7ZW5shyX0djcvD3+lfvKJmM1Zf7XqvSN4+tFpQ+snNVexXo/7VYgphjoXb/wvb/geAeXjV5MKf43Dh5A8gpbkktTzFGGh9R4Sq/FkEW57oBKemWSuh9kFlEHs7aqhstdwx20ry/oPi/Kb1Vd7INYmgIqlbn/AGqVE+zhUhMuDV6VcSjpC11lA+SS4VxflnigXz8vM1awUfHtiU0RMZ5fAaZ18clZfNFlTIOgSLincaQP4IaxPa2x4HySHaP+v4vM2jdxy9BODI2pn69B0VsMNkxrDAUSDfVVahcuxFd0RBInJfgOaFseqS1g/aydRF10PlWSjT6FUqA1Mql3rjz7VSZDyb/3Hn5BK4Nz9JzS1DxDNlb; BUC=Fge8ShcXw_mMccnewRPXBdaQ1HWsknjVath0ljJMdK4=',
        'logic': 'PART',
        'priority': 'u=1, i',
        'referer': 'https://search.shopping.naver.com/search/all?query=',
        'sbth': '309eeebb3ab42464c827e30f06f0d19a966adfdd658f066dc739229a7a4ddce6f61b110498a1cfacc7c78918163b7883',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-form-factors': '"Desktop"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.62", "Google Chrome";v="126.0.6478.62"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    params = {
        'adQuery': '줄눈셀프시공',
        'eq': '',
        'iq': '',
        'origQuery': '줄눈셀프시공',
        'pagingIndex': '2',
        'pagingSize': '40',
        'productSet': 'total',
        'query': '줄눈셀프시공',
        'sort': 'rel',
        'viewType': 'list',
        'window': '',
        'xq': '',
    }


    response = requests.get('https://search.shopping.naver.com/api/search/all', params=params, cookies=cookies, headers=headers) #기존코드

    # soup = BeautifulSoup(response.content, 'lxml')
    soup = response.json()
    # print(soup)
    # JSON 데이터를 문자열로 변환
    json_data = json.dumps(soup, indent=4,ensure_ascii=False)  # indent 옵션으로 보기 좋게 포맷팅
    with open("titles_json.txt", "w", encoding="utf-8") as file:
        file.write(json_data)

    for num in range(40):
        temp = soup["shoppingResult"]["products"][num]["rank"]
        print(str(temp)+ " 위")
        temp = soup["shoppingResult"]["products"][num]["productTitle"]
        print(temp)
    # import pandas as pd
    # df = pd.DataFrame(soup)
    # print(df)
    
if __name__ == "__main__":
    
    
    test2()