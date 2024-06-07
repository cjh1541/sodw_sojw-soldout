import mDriver_mode as mDriver
from selenium.webdriver.common.by import By

def driverInit():
    global driver
    driver = mDriver.make_driver('t2',mode='pc')
    
def test():
    driverInit()
    url = "https://www.jungoneshop.com/goods/goods_view.php?goodsNo=23701"
    driver.get(url)
    
    selector = "//button[@class='btn_add_order']"
    element = driver.find_element(By.XPATH, selector)

    temp = element.text
    print(temp)
    
if __name__ == "__main__":
    test()