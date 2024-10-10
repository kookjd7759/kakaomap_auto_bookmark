from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

url_kakao = 'https://map.kakao.com/'
url_bookmark_request = 'https://map.kakao.com/favorite/add.json'

xpath_btn_loginPage = '//*[@id="btnLogin"]'
xpath_btn_login = '//*[@id="mainContent"]/div/div/form/div[4]/button[1]'
xpath_btn_search = '//*[@id="search.keyword.submit"]'
xpath_btn_bookmark_banner = '/html/body/div[10]/div/div/div/span'
xpath_btn_group1 = '/html/body/div[20]/div[2]/div[2]/ul/li[2]'
color_List = ['red', 'yellow', 'orange', 'green', 'deep_green', 'purple', 'pink']
xpath_btn_color = {
    color_List[0] : '//*[@id="favoriteColor1"]',
    color_List[1] : '//*[@id="favoriteColor2"]',
    color_List[2] : '//*[@id="favoriteColor3"]',
    color_List[3] : '//*[@id="favoriteColor4"]',
    color_List[4] : '//*[@id="favoriteColor5"]',
    color_List[5] : '//*[@id="favoriteColor6"]',
    color_List[6] : '//*[@id="favoriteColor7"]'
}
xpath_btn_bookmark_enter = '/html/body/div[20]/div[3]/form/fieldset/div[3]/button'

xpath_input_ID = '//*[@id="loginId--1"]'
xpath_input_PASS = '//*[@id="password--2"]'
xpath_input_search = '//*[@id="search.keyword.query"]'

className_btn_menu = 'ico_toolbar'

def start(KAKAO_ID, KAKAO_PASS, color, filePath):
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)
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
            driver.execute_script("arguments[0].removeAttribute('readonly')", input_field)
            input_field.clear()
            input_field.send_keys(text)
            print(f'Input - {xpath}, {text}')
        except Exception as e:
            print(f'Input function failed :: {xpath}, {e}')

    def input_detail(title, memo):
        input('//*[@id="display1"]', title)
        input('//*[@id="favMemo"]', memo)

    click(xpath_btn_loginPage, By.XPATH)
    input(xpath_input_ID, KAKAO_ID)
    input(xpath_input_PASS, KAKAO_PASS)
    click(xpath_btn_login, By.XPATH)

    try:
        WebDriverWait(driver, 180).until(EC.visibility_of_element_located((By.XPATH, xpath_input_search)))
        print('Login !')
    except Exception as e:
        print('Login error', e)
    time.sleep(1)

    first = True
    def bookmark(index, address, name, count):
        nonlocal first
        input(xpath_input_search, address)
        click(xpath_btn_search, By.XPATH)
        if first:
            print('first bookmarking on this excution')
            click(xpath_btn_bookmark_banner, By.XPATH)
            first = False
        click(className_btn_menu, By.CLASS_NAME)
        click(xpath_btn_group1, By.XPATH)
        title = f'({index}) {name}'
        memo = f'{count} 장, {address}'

        input_detail(title, memo)
        click(xpath_btn_color[color], By.XPATH)
        click(xpath_btn_bookmark_enter, By.XPATH)

    df = pd.read_excel(filePath, sheet_name=0, engine='openpyxl')
    for _, row in df.iterrows():
        index = str(row[0])
        name = str(row[1])
        address = str(row[2])
        count = str(row[3])
        bookmark(index, address, name, count)

    while True:
        pass