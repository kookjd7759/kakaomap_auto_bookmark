from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url_kakao = 'https://map.kakao.com/'
url_bookmark_request = 'https://map.kakao.com/favorite/add.json'

xpath_btn_loginPage = '//*[@id="btnLogin"]'
xpath_btn_login = '//*[@id="mainContent"]/div/div/form/div[4]/button[1]'
xpath_btn_search = '//*[@id="search.keyword.submit"]'
xpath_btn_bookmark_banner = '/html/body/div[10]/div/div/div/span'
xpath_btn_group1 = '/html/body/div[20]/div[2]/div[2]/ul/li[2]'
xpath_btn_color = {
    'red'        : '//*[@id="favoriteColor1"]',
    'yellow'     : '//*[@id="favoriteColor2"]',
    'orange'     : '//*[@id="favoriteColor3"]',
    'green'      : '//*[@id="favoriteColor4"]',
    'deep_green' : '//*[@id="favoriteColor5"]',
    'purple'     : '//*[@id="favoriteColor6"]',
    'pink'       : '//*[@id="favoriteColor7"]'
}
xpath_btn_bookmark_enter = '/html/body/div[20]/div[3]/form/fieldset/div[3]/button'

xpath_input_ID = '//*[@id="loginId--1"]'
xpath_input_PASS = '//*[@id="password--2"]'
xpath_input_search = '//*[@id="search.keyword.query"]'

className_btn_menu = 'ico_toolbar'

KAKAO_ID = '01044587759'
KAKAO_PASS = 'rnrehdrbs1'

service = Service(ChromeDriverManager().install())
#chrome_options = Options()
#chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=service)#, options=chrome_options)
driver.get(url_kakao)

def click(src, by):
    try:
        if by == By.XPATH:
            button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((by, src)))
        elif by == By.CLASS_NAME:
            elements = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((by, src)))
            button = elements[0]
        
        driver.execute_script("arguments[0].click();", button)
        print(f'Click - {src}')
    except Exception as e:
        print(f'Click function failed :: CAN\'T CLICKED - {src}, {e}')

def input(xpath, text):
    try:
        input_field = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        input_field.clear()
        input_field.send_keys(text)
        print(f'Input - {xpath}, {text}')
    except Exception as e:
        print(f'Input function failed :: {xpath}, {e}')

click(xpath_btn_loginPage, By.XPATH)
input(xpath_input_ID, KAKAO_ID)
input(xpath_input_PASS, KAKAO_PASS)
click(xpath_btn_login, By.XPATH)

try:
    WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.XPATH, xpath_input_search)))
    print('Login !')
except Exception as e:
    print('Login error', e)
time.sleep(2)

first = True
color = 'red'
def bookmark(address):
    global first
    global color
    input(xpath_input_search, address)
    click(xpath_btn_search, By.XPATH)
    if first:
        print('first bookmarking on this excution')
        click(xpath_btn_bookmark_banner, By.XPATH)
        first = False
    click(className_btn_menu, By.CLASS_NAME)
    click(xpath_btn_group1, By.XPATH)
    click(xpath_btn_color[color], By.XPATH)
    click(xpath_btn_bookmark_enter, By.XPATH)

bookmark(address='경기 부천시 원미구 부천로 324')
bookmark(address='경기 부천시 원미구 부천로208번길 29')
bookmark(address='경기 부천시 원미구 부천로 342 부천시장애인직업재활시설')
bookmark(address='경기 부천시 원미구 도당동 산 25-5')
bookmark(address='경기 부천시 오정구 원종로93번길 39')

while True:
    pass