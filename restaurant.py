# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--window-size=1280x1696')
# chrome_options.add_argument('--user-data-dir=/tmp/user-data')
# chrome_options.add_argument('--hide-scrollbars')
# chrome_options.add_argument('--enable-logging')
# chrome_options.add_argument('--log-level=0')
# chrome_options.add_argument('--v=99')
# chrome_options.add_argument('--single-process')
# chrome_options.add_argument('--data-path=/tmp/data-path')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--homedir=/tmp')
# chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
# chrome_options.binary_location = "/opt/python/bin/headless-chromium"

# browser = webdriver.Chrome(options=chrome_options)

# last_button = WebDriverWait(browser, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '#page-selection > ul > li.last > a'))
#         )
# if last_button:
#     last_button.click()
#     time.sleep(2)

import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# 웹드라이버 설정
browser = webdriver.Chrome()
browser.get('https://www.bluer.co.kr/search?tabMode=single&searchMode=ribbonType&location=&ribbonType=RIBBON_ONE&feature=')
time.sleep(5)
resultset = []
def extract_data():
    cards = browser.find_elements(By.CLASS_NAME, 'thumb-caption')
    for card in cards:
        data = {}
        try:
            browser.execute_script("arguments[0].scrollIntoView();", card)
            time.sleep(0.5)
            WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(card)
            ).click()
            time.sleep(0.5)
            # 태그
            try:
                keyword = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#restaurant-view > div.restaurant-view-panel > header > div.pull-left > div.header-status'))
                ).text
                data['keyword'] = keyword
            except:
                data['keyword'] = None
            # 레스토랑 이름
            try:
                rest_name = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#restaurant-view > div.restaurant-view-panel > header > div.pull-left > div.header-title > h1'))
                ).text
                data['rest_name'] = rest_name
            except:
                data['rest_name'] = None
            # 전화번호
            try:
                rest_phone = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#restaurant-view > div.restaurant-view-panel > div > div.box-info.border.restaurant-info-1 > div > div.col-md-6.border-right-lg > dl > dd:nth-child(2) > a'))
                ).text
                data['rest_phone'] = rest_phone
            except:
                data['rest_phone'] = None
            # 주소
            try:
                rest_address = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#restaurant-view > div.restaurant-view-panel > div > div.box-info.border.restaurant-info-1 > div > div.col-md-6.border-right-lg > dl > dd:nth-child(4)'))
                ).text
                data['rest_address'] = rest_address
            except:
                data['rest_address'] = None
            # 영업시간
            try:
                rest_opentime = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#restaurant-view > div.restaurant-view-panel > div > div.box-info.border.restaurant-info-1 > div > div.col-md-6.padding-lg-left > dl > dd'))
                ).text
                data['rest_opentime'] = rest_opentime
            except:
                data['rest_opentime'] = None
            # 메뉴
            try:
                menu = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#restaurant-view > div.restaurant-view-panel > div > div.box-info.border.restaurant-info-3 > div > div.col-md-6.border-right-lg.restaurant-info-3-note-parent > dl:nth-child(1) > dd'))
                ).text
                data['menu'] = menu
            except:
                data['menu'] = None
            # 찾아가기
            try:
                find_path = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="restaurant-view"]//dl[dt="찾아가기"]/dd'))
                ).text
                data['find_path'] = find_path
            except:
                data['find_path'] = None
            # 특징
            try:
                feature = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="restaurant-view"]/div[1]/div/div[2]/div/div[2]/dl[dt="특징"]/dd'))
                ).text
                data['feature'] = feature
            except:
                data['feature'] = None
            # 이미지 URL 추출
            try:
                style_attr = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@class="owl-item active"]//li[@class="item restaurant-img bg-cover"]'))
                ).get_attribute('style')
                # 정규식을 사용하여 background-image의 URL 추출
                img_url = re.search(r'url\((.*?)\)', style_attr).group(1).strip("'\"")
                # 이미지 URL을 완전한 형식으로 구성
                if img_url.startswith('/'):
                    img_url = 'https://www.bluer.co.kr' + img_url
                data['image_url'] = img_url
            except Exception as e:
                data['image_url'] = None
            resultset.append(data)
            time.sleep(1)
            close_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#restaurant-view > div.restaurant-view-panel > header > div.btn-close'))
            )
            close_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"오류 발생: {e}")
            continue
current_page = 1
while True:
    extract_data()
    try:
        current_page += 1
        next_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'li[data-lp="{current_page}"] > a'))
        )
        next_button.click()
        time.sleep(2)
    except Exception as e:
        print("더 이상 페이지가 없습니다. 크롤링을 종료합니다.")
        break
# 브라우저 닫기
browser.quit()
# 결과를 파일에 쓰기 (JSON 형식)
with open("ribbon1.json", 'w', encoding='utf-8') as f:
    json.dump(resultset, f, ensure_ascii=False, indent=4)