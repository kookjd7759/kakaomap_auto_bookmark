from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pandas as pd

url_kakao = 'https://map.kakao.com/'
url_bookmark_request = 'https://map.kakao.com/favorite/add.json'

xpath_btn_loginPage = '//*[@id="btnLogin"]'
xpath_btn_login = '//*[@id="mainContent"]/div/div/form/div[4]/button[1]'
xpath_btn_search = '//*[@id="search.keyword.submit"]'
xpath_btn_bookmark_banner = '/html/body/div[10]/div/div/div/span'
def xpath_btn_group(idx):
    return f'/html/body/div[20]/div[2]/div[2]/ul/li[{idx + 1}]'
color_List = [
    'rgba(255, 93, 94, 1)',
    'rgba(255, 179, 1, 1)', 
    'rgba(255, 126, 27, 1)', 
    'rgba(47, 208, 70, 1)', 
    'rgba(18, 160, 95, 1)', 
    'rgba(153, 129, 255, 1)', 
    'rgba(241, 121, 220, 1)', 
    ]
def xpath_btn_color(idx):
    return f'//*[@id="favoriteColor{idx + 1}"]'
xpath_btn_bookmark_enter = '/html/body/div[20]/div[3]/form/fieldset/div[3]/button'
xpath_btn_my = '//*[@id="search.tab5"]'
xpath_input_ID = '//*[@id="loginId--1"]'
xpath_input_PASS = '//*[@id="password--2"]'
xpath_input_search = '//*[@id="search.keyword.query"]'

className_btn_menu = 'ico_toolbar'

def start(KAKAO_ID, KAKAO_PASS, color_idx, filePath, group):
    all = 0
    success = 0
    fail = 0
    Failed_data = {
        'Index': [],
        'Name': [],
        'Address': [],
        'Count' : [],
        'Log' : []
    }
    failed_size = 0
    def append_failed(index, name, address, count, log):
        nonlocal failed_size
        failed_size += 1
        Failed_data['Index'].append(index)
        Failed_data['Name'].append(name)
        Failed_data['Address'].append(address)
        Failed_data['Count'].append(count)
        Failed_data['Log'].append(log)

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
            return -1, -1, -1

    def input(xpath, text):
        try:
            input_field = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].removeAttribute('readonly')", input_field)
            input_field.clear()
            input_field.send_keys(text)
            print(f'Input - {xpath}, {text}')
        except Exception as e:
            print(f'Input function failed :: {xpath}, {e}')
            return -1, -1, -1

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

    def isDuplicate():
        try:
            WebDriverWait(driver, 0.3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.num.num1')))
            return True
        except:
            return False
    
    first = True
    def bookmark(index, name, address, count):
        nonlocal all
        nonlocal success
        nonlocal fail
        nonlocal first
        all += 1
        input(xpath_input_search, address)
        click(xpath_btn_search, By.XPATH)
        if first:
            print('first bookmarking on this excution')
            click(xpath_btn_bookmark_banner, By.XPATH)
            first = False
        time.sleep(0.3)
        if isDuplicate():
            print('Duplicate !')
            append_failed(index, name, address, count, '중복된 주소')
            fail += 1
        else:
            click(className_btn_menu, By.CLASS_NAME)
            click(xpath_btn_group(group), By.XPATH)
            title = f'({index}) {name}'
            memo = f'{count} 장, {address}'

            input_detail(title, memo)
            click(xpath_btn_color(color_idx), By.XPATH)
            click(xpath_btn_bookmark_enter, By.XPATH)
            success += 1

    df = pd.read_excel(filePath, sheet_name=0, engine='openpyxl')
    for _, row in df.iterrows():
        index = str(row[0])
        name = str(row[1])
        address = str(row[2])
        count = str(row[3])
        bookmark(index, name, address, count)

    if failed_size != 0:
        df = pd.DataFrame(Failed_data)
        file_path = os.getcwd() + '\\kakaomap_auto_bookmark\\failed.xlsx'
        df.to_excel(file_path, index=False, engine='openpyxl')

    driver.close()
    return all, success, fail

if __name__ == '__main__':
    start('01044587759', 'rnrehdrbs1', 0, 'C:\\WorkSpace\\Visual Studio Code Workspace\\kakaomap_auto_bookmark\\test_bookmarkList(xlsx).xlsx', 2)