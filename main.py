#### Imports Region ####
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


#### Data Region ####
PRODUCTS_DICT = {
    "5411188134985" : {
        "Name" : "Not Milk",
        "Amount" : "2"
    },
    "1491096" : {
        "Name" : "Green Tea",
        "Amount" : "2"
    }
}

USERNAME = "***REMOVED***"

PASSWORD = "***REMOVED***"

URL = 'https://www.shufersal.co.il/online/he/login'


#### Functions Region ####
def open_website():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(800, 1080)
    driver.get(URL)
    return driver

def sign_in(driver, username, password):
    search_box = driver.find_element(By.ID, "j_username")
    search_box.send_keys(username)

    search_box = driver.find_element(By.ID, "j_password")
    search_box.send_keys(password)
    search_box.send_keys(Keys.ENTER)  
    
    time.sleep(5)   

def clear_cart(driver):
     
    add_btn = driver.find_element(By.CSS_SELECTOR,".mobileTop.openCart.hidden-lg-header")
    add_btn.click()
    
    time.sleep(2)

    if found_elements := driver.find_elements(By.CSS_SELECTOR, '.col-xs-6.deleteCartContainer'):
        add_btn = found_elements[0]
        add_btn.click()
        
        time.sleep(2)

        add_btn = driver.find_element(By.CSS_SELECTOR,".btn-radius.outline")
        add_btn.click()
        
        time.sleep(2)

    add_btn = driver.find_element(By.CSS_SELECTOR,".closeCart.btnClose")
    add_btn.click()

def add_item(driver, barcode):
    search_box = driver.find_element(By.ID, "js-site-search-input")
    search_box.click()
    search_box.send_keys(Keys.CONTROL + "a")
    search_box.send_keys(Keys.DELETE)    
    
    time.sleep(2)

    search_box.send_keys(barcode)
    search_box.send_keys(Keys.ENTER)
    
    # add_btn = driver.find_element(By.CSS_SELECTOR,".btn.js-add-to-cart.js-enable-btn.miglog-btn-add")
    add_btn = driver.find_element(By.XPATH,'//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/button[1]')
    
    add_btn.click()

def add_items(driver, products_dict):

    for k, v in products_dict.items():
        add_item(driver, k)
        time.sleep(3)

def keep_alive():
    # keep chrome alive
    while(True):
        pass

def to_impl():
    pass

def main():
    driver = open_website()

    sign_in(driver, USERNAME, PASSWORD)

    clear_cart(driver)

    add_items(driver, PRODUCTS_DICT)

    to_impl()

    keep_alive()


#### Main Region ####
main()


#### Tasks Region ####
# (v) Fix add_item(...) for 2nd item - Fixed with XPATH 
# (-) Implement the rest, use as many functions as needed
# (-) Test with a full basket
# (-) Split open_website() to init_browser(...) and goto_url(...)
# (-) Final payment must always be manual after cart review !!!!!!
# (-) What else? Who else?