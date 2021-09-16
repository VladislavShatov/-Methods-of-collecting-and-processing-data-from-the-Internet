from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import ast

client = MongoClient('localhost', 27017)
db = client['dz']
m_video = db['m_video']
chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
actions = ActionChains(driver)
driver.get("https://www.mvideo.ru/")
new_products = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]")
actions.move_to_element(new_products).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN) \
    .key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN) \
    .key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN)
# можно было бы и перейти к элементу ниже, но в случае, если у сайта изментися структура - этот вариант самый подходящий
# хоть и не очень красивый
actions.perform()
a = True
b = 0
description_data = {}
while a:
    try:
        data = driver.find_elements_by_xpath(
            "//h2[contains(text(), 'Новинки')]/parent::*/parent::*/parent::*//div[contains(@class, 'fl-product-tile__picture-holder c-product-tile-picture__holder')]//a")
        while b != len(data):
            product_description = dict(ast.literal_eval(data[b].get_attribute('data-product-info')))
            description_data['_id'] = b
            description_data['Name'] = product_description['productName']
            description_data['Category'] = product_description['productCategoryName']
            description_data['Vendor'] = product_description['productVendorName']
            description_data['Price'] = product_description['productPriceLocal']
            result = m_video.insert_one(description_data)

            b += 1
            print (b)
        wait = WebDriverWait(driver, 5)
        button_wait = wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             "//h2[contains(text(), 'Новинки')]/parent::*/parent::*/parent::*//a[contains(@class,'next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right')]")

        ))
        button_wait.click()
    except TimeoutException:
        a = False
