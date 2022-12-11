#### Imports Region ####
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


#### Data Region ####
RES_DICT = {
    "user_box" : 'j_username',
    "pass_box" : 'j_password',
    "cart_btn" : '//*[@id="main"]/div[1]/section/ul/li[5]/a/div',
    "del_btn" : '.col-xs-6.deleteCartContainer',
    "del2_btn" : ".btn-radius.outline",
    "search_box" : "js-site-search-input",
    "close_btn" : ".closeCart.btnClose",
    "amount_box" : '//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/div[3]/div[1]/input',
    "add_btn" : '//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/button[1]',
    "pay_btn" : '//*[@id="cartContainer"]/div[1]/div/footer/div[2]/div/div[3]',
    "check_btn" : '//*[@id="cartContainer"]/div/div/footer/div[2]/div/div[2]/button',
}

PROD_DICT = {
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
    # "3726776" : {
    #     "Name" : "Tofu Schnitzel",
    #     "Amount" : "1"
    # },
    # "7290017105895" : {
    #     "Name" : "Hummus Can",
    #     "Amount" : "1"
    # },
    # "7296073006411" : {
    #     "Name" : "Medium Pickles",
    #     "Amount" : "1"
    # },
    # "7296073345763" : {
    #     "Name" : "Organic Tofu",
    #     "Amount" : "1"
    # },
    # "7296073392699" : {
    #     "Name" : "Paper Towels",
    #     "Amount" : "4"
    # },
    # "187938" : {
    #     "Name" : "Toilet Paper",
    #     "Amount" : "1"
    # },
    # "7290013724946" : {
    #     "Name" : "Chocolate Almonds",
    #     "Amount" : "1"
    # }
}

USERNAME = "user"

PASSWORD = "pass"

URL = 'https://www.shufersal.co.il/online/he/login'

WIN_WIDTH = 800
WIN_HEIGHT = 800
#### Functions Region ####
def init_website(win_width, win_height):
    # our handle for the chrome browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(win_width, win_height)
    return driver

def goto_url(driver, url):
    driver.get(url)

def sign_in(driver, username, password):
    user_box = driver.find_element(By.ID, RES_DICT['user_box'])
    user_box.send_keys(username)

    pass_box = driver.find_element(By.ID, RES_DICT['pass_box'])
    pass_box.send_keys(password)
    pass_box.send_keys(Keys.ENTER)  
    
    # wait until post-login notification dissappears 
    time.sleep(5)   

def view_cart(driver):
    cart_btn = driver.find_element(By.XPATH, RES_DICT['cart_btn'])
    cart_btn.click()

    time.sleep(2) #TODO: Is sleep needed?

def clear_cart(driver):
    # handle missing button when cart is empty
    if found_elements := driver.find_elements(By.CSS_SELECTOR, RES_DICT['del_btn']):
        del_btn = found_elements[0]
        
        # click on clear cart
        del_btn.click()
        
        time.sleep(2) #TODO: Is sleep really needed?

        # click to approve clear cart
        del2_btn = driver.find_element(By.CSS_SELECTOR, RES_DICT['del2_btn'])
        del2_btn.click()
        
        time.sleep(2) #TODO: Is sleep really needed?

    close_btn = driver.find_element(By.CSS_SELECTOR, RES_DICT['close_btn'])
    close_btn.click()

def find_item(driver, barcode):
    search_box = driver.find_element(By.ID, RES_DICT['search_box'])
    search_box.click()
    
    # clear text box
    search_box.send_keys(Keys.CONTROL + "a")
    search_box.send_keys(Keys.DELETE)    
    
    # search item
    search_box.send_keys(barcode)
    search_box.send_keys(Keys.ENTER)

def enter_amount(driver, barcode):
    amount_box = driver.find_element(By.XPATH, RES_DICT['amount_box'])
    amount_box.click()

    # clear text box
    amount_box.send_keys(Keys.ARROW_UP)   
    amount_box.send_keys(Keys.BACK_SPACE)   
    
    # enter amount
    amount_box.send_keys(int(PROD_DICT[barcode]['Amount']))
    amount_box.click()

def set_cart(driver):
    # actual add item to cart
    add_btn = driver.find_element(By.XPATH, RES_DICT['add_btn'])
    add_btn.click()

def add_item(driver, barcode):
    find_item(driver, barcode)
    enter_amount(driver, barcode)        
    set_cart(driver)

def add_items(driver, products_dict):
    for barcode, data_dict in products_dict.items():
        add_item(driver, barcode)
        time.sleep(3) #TODO: Is sleep really needed?

def pay_cart(driver):
    pay_btn = driver.find_element(By.XPATH, RES_DICT['pay_btn'])
    pay_btn.click()

    check_btn = driver.find_element(By.XPATH, RES_DICT['check_btn']) 
    check_btn.click()

    time.sleep(2) #TODO: Is sleep needed?

def pass_approve(driver, password):
    pass_box = driver.find_element(By.ID, RES_DICT['pass_box'])
    pass_box.send_keys(password)
    pass_box.send_keys(Keys.ENTER)

def keep_alive():
    # keep chrome alive
    while(True):
        pass

def main():
    driver = init_website(WIN_WIDTH, WIN_HEIGHT)

    goto_url(driver, URL)

    sign_in(driver, USERNAME, PASSWORD)

    view_cart(driver)
    
    clear_cart(driver)

    add_items(driver, PROD_DICT)

    view_cart(driver)

    pay_cart(driver)
    
    pass_approve(driver, PASSWORD)

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
# (-) Missing item exception
# (-) Json file product dict
# (-) Store passwords
# (*) Final payment must always be manual after cart review !!!!!!
# (*) When done: Vegetables, Peanut, Vegan Supplies, Super Pharm