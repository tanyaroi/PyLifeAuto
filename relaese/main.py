#### Imports Region ####
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import pwinput


#### Data Region ####
RES_DICT_PATH = "res_dict.json"

PROD_DICT_PATH = 'prod_dict.json'

URL = 'https://www.shufersal.co.il/online/he/login'

WIN_WIDTH = 800
WIN_HEIGHT = 800

#### Functions Region ####
def load_prod_dict(prod_dict_path):

    prod_dict = {}

    with open(prod_dict_path) as prod_dict_handle:
        prod_dict_nested = json.load(prod_dict_handle)

        for prod_dict_sub in prod_dict_nested.values():
            prod_dict.update(prod_dict_sub)

    return prod_dict


def load_res_dict(res_dict_path):
    res_dict = {}

    with open(res_dict_path) as res_dict_handle:
        res_dict = json.load(res_dict_handle)
    
    return res_dict


def get_creds():
    time.sleep(1)

    username = input("Username: ")
    password = pwinput.pwinput(prompt = "Password: ", mask = "*")
    
    return username, password


def init_website(win_width, win_height):
    # our handle for the chrome browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(win_width, win_height)
    return driver


def goto_url(driver, url):
    driver.get(url)


def sign_in(driver, res_dict, username, password):
    user_box = driver.find_element(By.ID, res_dict['user_box'])
    user_box.send_keys(username)

    pass_box = driver.find_element(By.ID, res_dict['pass_box'])
    pass_box.send_keys(password)
    pass_box.send_keys(Keys.ENTER)  
    
    # wait until post-login notification dissappears 
    time.sleep(5)   


def view_cart(driver, res_dict):
    cart_btn = driver.find_element(By.XPATH, res_dict['cart_btn'])
    cart_btn.click()

    time.sleep(2) #TODO: Is sleep needed?


def clear_cart(driver, res_dict):
    # handle missing button when cart is empty
    if found_elements := driver.find_elements(By.CSS_SELECTOR, res_dict['del_btn']):
        del_btn = found_elements[0]
        
        # click on clear cart
        del_btn.click()
        
        time.sleep(2) #TODO: Is sleep really needed?

        # click to approve clear cart
        del2_btn = driver.find_element(By.CSS_SELECTOR, res_dict['del2_btn'])
        del2_btn.click()
        
        time.sleep(2) #TODO: Is sleep really needed?

    close_btn = driver.find_element(By.CSS_SELECTOR, res_dict['close_btn'])
    close_btn.click()


def find_item(driver, res_dict, barcode):
    search_box = driver.find_element(By.ID, res_dict['search_box'])
    search_box.click()
    
    # clear text box
    search_box.send_keys(Keys.CONTROL + "a")
    search_box.send_keys(Keys.DELETE)    
    
    # search item
    search_box.send_keys(barcode)
    search_box.send_keys(Keys.ENTER)

    return not driver.find_elements(By.XPATH, res_dict['nosearch_img'])


def enter_amount(driver, res_dict, prod_dict, barcode):
    amount_box = driver.find_element(By.XPATH, res_dict['amount_box'])
    amount_box.click()

    # clear text box
    amount_box.send_keys(Keys.ARROW_UP)   
    amount_box.send_keys(Keys.BACK_SPACE)   
    
    # enter amount
    amount_box.send_keys(int(prod_dict[barcode]['Amount']))
    amount_box.click()


def set_cart(driver, res_dict):
    # actual add item to cart
    add_btn = driver.find_element(By.XPATH, res_dict['add_btn'])
    add_btn.click()


def add_item(driver, res_dict, prod_dict, barcode):
    if not find_item(driver, res_dict, barcode):
        raise Exception("Invalid barcode")
    
    enter_amount(driver, res_dict, prod_dict, barcode)        
    set_cart(driver, res_dict)


def add_items(driver, res_dict, prod_dict):
    for barcode, data_dict in prod_dict.items():
        add_item(driver, res_dict, prod_dict, barcode)
        time.sleep(3) #TODO: Is sleep really needed?


def pay_cart(driver, res_dict):
    pay_btn = driver.find_element(By.XPATH, res_dict['pay_btn'])
    pay_btn.click()

    check_btn = driver.find_element(By.XPATH, res_dict['check_btn']) 
    check_btn.click()

    time.sleep(2) #TODO: Is sleep needed?


def pass_approve(driver, res_dict, password):
    pass_box = driver.find_element(By.ID, res_dict['pass_box'])
    pass_box.send_keys(password)
    pass_box.send_keys(Keys.ENTER)


def keep_alive():
    # keep chrome alive
    while(True):
        pass


def main():
    username, password = get_creds()
    
    res_dict = load_res_dict(RES_DICT_PATH)

    prod_dict = load_prod_dict(PROD_DICT_PATH)
    
    driver = init_website(WIN_WIDTH, WIN_HEIGHT)

    goto_url(driver, URL)

    sign_in(driver, res_dict, username, password)

    view_cart(driver, res_dict)
    
    clear_cart(driver, res_dict)

    add_items(driver, res_dict, prod_dict)

    view_cart(driver, res_dict)

    pay_cart(driver, res_dict)
    
    pass_approve(driver, res_dict, password)

    keep_alive()


#### Main Region ####
main()


#### Tasks Region ####
# (v) Fix add_item(...) for 2nd item - Fixed with XPATH 
# (v) Implement the rest, use as many functions as needed
# (v) Test with a full basket
# (v) Add amount functionality
# (v) Code refactor (naming, divide to functions, comments, global variables)
# (v) Split open_website() to init_browser(...) and goto_url(...)
# (v) Json files for res_dict and product dict
# (v) Missing item exception
# (*) Final payment must always be manual after cart review !!!!!!
# (*) When done: Vegetables, Peanut, Vegan Supplies, Super Pharm