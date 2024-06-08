import random,os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from user_agents import parse
from selenium.webdriver import ActionChains

def make_user_agent(ua,is_mobile):
    user_agent = parse(ua)
    model = user_agent.device.model
    platform = user_agent.os.family
    platform_version = user_agent.os.version_string + ".0.0"
    version = user_agent.browser.version[0]
    ua_full_version = user_agent.browser.version_string
    architecture = "x86"
    print(platform)
    if is_mobile:
        platform_info = "Linux armv8l"
        architecture= ""
    else: # Window
        platform_info = "Win32"
        model = ""
    RET_USER_AGENT = {
        "appVersion" : ua.replace("Mozilla/", ""),
        "userAgent": ua,
        "platform" : f"{platform_info}",
        "acceptLanguage" : "ko-KR, kr, en-US, en",
        "userAgentMetadata":{
            "brands" : [
                {"brand":"Google Chrome", "version":f"{version}"},
                {"brand":"Chromium", "version":f"{version}"},
                {"brand":"Not A;Brand", "version":"99"},
            ],
            "fullVersionList":[
                {"brand":"Google Chrome", "version":f"{version}"},
                {"brand":"Chromium", "version":f"{version}"},
                {"brand":"Not A;Brand", "version":"99"},
            ],
            "fullVersion":f"{ua_full_version}",
            "platform" :platform,
            "platformVersion":platform_version,
            "architecture":architecture,
            "model" : model,
            "mobile":is_mobile #True, False
        }
    }
    return RET_USER_AGENT

def read_agents():
    agents = []
    f = open("./useragents.txt","r",encoding="utf8")
    while True:
        line = f.readline()
        if not line:
            break
        agents.append(line.rstrip())
    return agents

def make_driver(account_id,mode='mo'):
    try:
        pc_device = ["1920,1440","1920,1200","1920,1080","1600,1200","1600,900",
                        "1536,864", "1440,1080","1440,900","1360,768"
                ]

        mo_device = [
                    "360,640", "360,740", "375,667", "375,812", "412,732", "412,846",
                    "412,869", "412,892", "412,915"
                ]

        if mode == "mo":
            width,height = random.choice(mo_device).split(",")
        elif mode == "pc":
            width,height = random.choice(pc_device).split(",")

        if mode == 'mo':
            UA_list = read_agents()
            UA = random.choice(UA_list)  #seed = time.time()
        elif mode == 'pc':
            # 테스트용 pc버전 UA 
            # user agent list 더 많이 확보해 보기
            UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        
        options = uc.ChromeOptions()

        #폴더가 없다면, 생성
        folder = os.path.join('C:\\',"cookies")
        if not os.path.exists(folder):
            os.makedirs(folder)
        cookie_folder_name = os.path.join(folder, account_id)
        if not os.path.exists(cookie_folder_name):
            os.makedirs(cookie_folder_name)

        #작업별 쿠키 기록을 남김
        # options.user_data_dir = cookie_folder_name

        # User Agent 속이기
        options.add_argument(f'--user-agent={UA}')
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
        options.add_argument('--disable-logging')
        options.headless = True #add this line 기존코드
        
        #테스트용 추가
        # options.add_argument('--headless')  # 브라우저 창을 띄우지 않음
        # options.add_argument('--disable-gpu')
        
        
        # 크롬드라이버 수동 설정 
        # chromedriver_path = r"C:/python_work/230314_esselers/test/chromedriver.exe"
        # driver = uc.Chrome(driver_executable_path=chromedriver_path,user_data_dir=cookie_folder_name,options=options,)
        
        # 기존 코드
        driver = uc.Chrome(user_data_dir=cookie_folder_name,options=options,)
        
        if mode == 'mo':
            UA_Data = make_user_agent(UA,True)

            driver.execute_cdp_cmd("Network.setUserAgentOverride",UA_Data)

            # Max Touch Point 변경
            Mobile = {"enabled":True, "maxTouchPoints": random.choice([1,5])}
            driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled",Mobile)
            driver.execute_cdp_cmd("Emulation.setNavigatorOverrides",{"platform":"Linux armv8l"})
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                "width":int(width),
                "height":int(height),
                "deviceScaleFactor":1,
                "mobile" : True
            })
        elif mode == 'pc':
            UA_Data = make_user_agent(UA,False)

            driver.execute_cdp_cmd("Network.setUserAgentOverride",UA_Data)

            # Max Touch Point 변경
            Mobile = {"enabled":True, "maxTouchPoints": random.choice([1,5])}
            # driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled",Mobile)
            driver.execute_cdp_cmd("Emulation.setNavigatorOverrides",{"platform":"Linux armv8l"})
            driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",{
                "width":int(width),
                "height":int(height),
                "deviceScaleFactor":1,
                "mobile" : True
            })

        # 위치 정보 변경 Geo Location 변경하기
        def generate_random_geolocation():
            ltop_lat = 37.75415601640249
            ltop_long = 126.86767642302573
            rbottom_lat = 37.593829172663945
            rbottom_long = 127.15276051439332

            targetLat = random.uniform(rbottom_lat, ltop_lat)
            targetLong = random.uniform(ltop_long,rbottom_long)
            return {"latitude":targetLat, "longitude" : targetLong, "accuracy":100}
        GEO_DATA = generate_random_geolocation()
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", GEO_DATA)

        # User Agent 적용
        driver.execute_cdp_cmd("Emulation.setUserAgentOverride",UA_Data)
        print(width,height)
        driver.set_window_size(int(width),int(height))
        
        return driver
    except Exception as e:
        print(e)
        driver = None
        return driver