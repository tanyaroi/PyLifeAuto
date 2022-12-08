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
    "54051157" : {
        "Name" : "Chocolate Vegangurt",
        "Amount" : "2"
    },
    "7296073205692" : {
        "Name" : "Tomato Sauce",
        "Amount" : "1"
    },
    "3726776" : {
        "Name" : "Tofu Schnitzel",
        "Amount" : "1"
    },
    "7290017105895" : {
        "Name" : "Hummus Can",
        "Amount" : "1"
    },
    "7296073006411" : {
        "Name" : "Medium Pickles",
        "Amount" : "1"
    },
    "7296073345732" : {
        "Name" : "Organic Tofu",
        "Amount" : "1"
    },
    "7296073392699" : {
        "Name" : "Paper Towels",
        "Amount" : "4"
    },
    "187938" : {
        "Name" : "Toilet Paper",
        "Amount" : "1"
    },
    "7290013724946" : {
        "Name" : "Chocolate Almonds",
        "Amount" : "1"
    }
}

USERNAME = "***REMOVED***"

PASSWORD = "***REMOVED***"

URL = 'https://www.shufersal.co.il/online/he/login'


#### Functions Region ####
def open_website():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(800, 800)
    driver.get(URL)
    return driver

def sign_in(driver, username, password):
    search_box = driver.find_element(By.ID, "j_username")
    search_box.send_keys(username)

    search_box = driver.find_element(By.ID, "j_password")
    search_box.send_keys(password)
    search_box.send_keys(Keys.ENTER)  
    
    time.sleep(5)   

def open_cart(driver):
    
    add_btn = driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/ul/li[5]/a/div')
    add_btn.click()
    
    time.sleep(2)

def clear_cart(driver):

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

def cart_pay(driver):
    add_btn = driver.find_element(By.XPATH,'//*[@id="cartContainer"]/div[1]/div/footer/div[2]/div/div[3]')
    add_btn.click()

    add_btn = driver.find_element(By.XPATH,'//*[@id="cartContainer"]/div/div/footer/div[2]/div/div[2]/button') 
    add_btn.click()

    time.sleep(2)

def pass_approve(driver, password):
    search_box = driver.find_element(By.ID, "j_password")
    search_box.send_keys(password)
    search_box.send_keys(Keys.ENTER)

def keep_alive():
    # keep chrome alive
    while(True):
        pass

def main():
    driver = open_website()

    sign_in(driver, USERNAME, PASSWORD)

    open_cart(driver)
    
    clear_cart(driver)

    add_items(driver, PRODUCTS_DICT)

    open_cart(driver)

    cart_pay(driver)
    
    pass_approve(driver, PASSWORD)

    keep_alive()


#### Main Region ####
main()


#### Tasks Region ####
# (v) Fix add_item(...) for 2nd item - Fixed with XPATH 
# (v) Implement the rest, use as many functions as needed
# (-) Test with a full basket
# (-) Add amount functionality
# (-) Missing item exception
# (-) Json file product dict
# (-) Split open_website() to init_browser(...) and goto_url(...)
# (-) Final payment must always be manual after cart review !!!!!!
# (-) What else? Who else?