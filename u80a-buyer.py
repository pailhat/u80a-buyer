
# This script tries to buy a U80-A Seq1 Extra when they go live on Oct 10, 2020 at 10pm PDT on https://ramaworks.store using google chrome.
# Run this before the boards are set to go live, like a few minutes is fine. It will wait and checkout for you.

# Edit the stuff below before running.

# DOWNLOAD THIS FIRST FOR YOUR VERSION OF CHROME https://sites.google.com/a/chromium.org/chromedriver/downloads
# AND EXTRACT IT SOMEWHERE. The file extracted is called chromedriver.exe.
# Path to chromedriver.exe:
PATH = "C:/Users/You/Anywhere/chromedriver.exe"

# Enter your info for completing checkout. Follow the exact format of the examples.
EMAIL = "myemail123@gmail.com"

FIRST_NAME = "John"
LAST_NAME = "Doe"
ADDRESS = "123 Nicestreet Ave"
ADDRESS_2 = "" # If you don't need this leave blank
CITY = "Albany" # Type this exactly as it appears in the ramaworks.store checkout dropdown list
COUNTRY =  "United States" # Type this exactly as it appears in the ramaworks.store checkout dropdown list
STATE = "New York" # Type this exactly as it appears in the ramaworks.store checkout dropdown list
ZIP_CODE = "12345" # 5 digit zip code
PHONE = "1231231234" # 3 digit area code + phone number

CARD_NUMBER = "1234432112344321" # 16 Digit card number no spaces
NAME_ON_CARD = "JOHN DOE"
CARD_EXPIRATION_DATE = "01/23" # MM/YY
CARD_SECURITY_CODE = "123" # 3 digit number on back of card

# Choose Color and PCB combo in order of preference from left to right.
# It'll only buy one, but this is just in case there are no extras available for your most
# preferred color the bot will pick your next best preference.
# leftmost = want the most
# Add more choices if you want
COLOR_CHOICE = ["kuro","LAKE","MILK","MILK","PORT","PORT"] # KURO, MOON, LAKE, PORT, MILK are the options for seq1
PCB_CHOICE = ["Hotswap","Solderable","Hotswap","Solderable","Hotswap","Solderable"] # Hotswap, Solderable


# *************** BEGIN SCRIPT DONT EDIT ANYTHING BELOW THIS *************** #

import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Open Chrome and wait until U80A Extras are posted on the product page
driver = webdriver.Chrome(PATH)
URL = "https://ramaworks.store/products/u80-a-seq2"

driver.get(URL)

# 10th 10PM PDT = 11th 5AM UTC = 11th 1am EDT
# UTC time for rama U80A extra release
# Year,Month,Day,Hour,Minute
release_time = datetime(2020,10,11,5) 

print("Waiting for 10AM PDT...")

while True:
    if datetime.utcnow() >= release_time:
        break
    time.sleep(0.05)

start_time = time.time()

# Selects the option you wanted
try:
    # Rama redirects you to ramaworks.store/password if the page is not yet available
    while True:
        driver.get(URL)
        time.sleep(0.1)
        if driver.current_url == URL:
            break

    # Wait until the page loads and we can see the color options and add to cart button
    # Just in case the add to cart button is disabled because they didn't add the product stock at exactly the same time
    # as unlocking the page, we refresh until its enabled.
    while True:
        driver.get(URL)
        add_to_cart_button = WebDriverWait(driver, 10, poll_frequency=0.01).until(
            EC.presence_of_element_located((By.ID, "addToCart-product-template"))
        )
        if add_to_cart_button.is_enabled():
            break

    option_list = WebDriverWait(driver, 10, poll_frequency=0.05).until(
        EC.presence_of_element_located((By.ID, "ProductSelect-option-0"))
    )

    # Loop through the Color options and click the label that matches what you want
    # It will try to get your most preferred color/pcb combo. It will try each combo in the list until it finds an available one.
    options = option_list.find_elements_by_tag_name("label")
    found = False
    for i in range(len(COLOR_CHOICE)):
        for label in options:
            # Converted everything to lowercase and searched for the color and pcb option separately in the string instead of matching the 
            # label exactly. Just in case they changed the labels or the capitalization from the old listing it wont foil the bot
            if (COLOR_CHOICE[i].lower() in label.text.lower()) and (PCB_CHOICE[i].lower() in label.text.lower()):                
                if (label.get_attribute("class") == "disabled"):
                    # If the input was disabled that means that choice is out of stock/unavailable
                    print(COLOR_CHOICE[i] + " (" + PCB_CHOICE[i] + ") was not available.")    
                else:
                    # If the input is enabled then we can select it by clicking and continue.
                    label.click()
                    print("Selected: " + label.text)
                    found = True
                break
        else:
            print(COLOR_CHOICE[i] + " (" + PCB_CHOICE[i] + ") was not not found.")

        if found:
            break

    # If it couln't find any of the options that you wanted I hope ur fingers r fast u have to do it manually :(
    if not found:
        print("Couldn't purchase your selection sorry :(")
        exit()

    # Add to cart.
    add_to_cart_button.click()
    
    # Wait until the page loads and we can see the checkout button before clicking
    checkout_button = WebDriverWait(driver, 10, poll_frequency=0.05).until(
        EC.presence_of_element_located((By.NAME, "checkout"))
    )

    print("Checkout button located!")

    while not checkout_button.is_enabled() or not  checkout_button.is_displayed():
        print("Checkout disabled will click when its enabled")

    checkout_button.click()



    # Enter your shipping info
    # Wait until the page loads and we can see the continue button, then the form should be loaded and we can enter stuff
    continue_button = WebDriverWait(driver, 10, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.ID, "continue_button"))
    )


    input_email = driver.find_element_by_id("checkout_email")
    input_first_name = driver.find_element_by_id("checkout_shipping_address_first_name")
    input_last_name = driver.find_element_by_id("checkout_shipping_address_last_name")
    input_address = driver.find_element_by_id("checkout_shipping_address_address1")
    input_address_2 = driver.find_element_by_id("checkout_shipping_address_address2")
    input_city = driver.find_element_by_id("checkout_shipping_address_city")
    input_country = driver.find_element_by_id("checkout_shipping_address_country")
    input_state = driver.find_element_by_id("checkout_shipping_address_province")
    input_zip_code = driver.find_element_by_id("checkout_shipping_address_zip")
    input_phone = driver.find_element_by_id("checkout_shipping_address_phone")

    input_email.send_keys(EMAIL)
    input_first_name.send_keys(FIRST_NAME)
    input_last_name.send_keys(LAST_NAME)
    input_address.send_keys(ADDRESS)
    input_address_2.send_keys(ADDRESS_2)
    input_city.send_keys(CITY)
    input_country.send_keys(COUNTRY)
    input_country.send_keys(Keys.TAB)
    input_state.send_keys(STATE)
    input_state.send_keys(Keys.TAB)
    input_zip_code.send_keys(ZIP_CODE)
    input_phone.send_keys(PHONE)

    continue_button.click()

    # The least expensive shipping option is selected by default. We just press the continue button again once it loads to continue to
    # enter payment info.

    # Wait until the page loads and we can see the shipping options & new continue button, then we can press continue to payment
    shipping_label = WebDriverWait(driver, 10, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.CLASS_NAME, "radio__label"))
    )
    print(shipping_label.text)
    continue_button = WebDriverWait(driver, 10, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.ID, "continue_button"))
    )
    continue_button.click()


    # Enter credit card info after the pay now button appears, then hit pay now
    # Wait until the page loads and we can see the pay now button
    pay_now_button = WebDriverWait(driver, 10, poll_frequency=0.1).until(
        EC.presence_of_element_located((By.ID, "continue_button"))
    )

except ValueError:
    print(ValueError)

# Each credit cart field is in its own iframe, so we can only access it by its id once 
# we switch focus to the iframe its in.

# Get the 4 card input iframes in a list using their class name
card_iframes = driver.find_elements_by_class_name("card-fields-iframe")

# The ID of the iframe tells us what card field we will find in it
# the iframe ID will look like this:
# card-fields-verification_value-dskjjk432000000
field_map = {
    'card-fields-number': {'input_id': 'number', 'value': CARD_NUMBER},
    'card-fields-name': {'input_id': 'name', 'value': NAME_ON_CARD},
    'card-fields-expiry': {'input_id': 'expiry', 'value': CARD_EXPIRATION_DATE},
    'card-fields-verification_value': {'input_id': 'verification_value', 'value': CARD_SECURITY_CODE},
    }

for iframe in card_iframes:
    # Get rid of the gibberish at the end of the iframe ID, since it will be unique for each checkout
    iframe_id = iframe.get_attribute("id")[0:iframe.get_attribute("id").rindex("-")]
    driver.switch_to.frame(iframe)

    # Fill in the field
    # Instead of sending characters, copy paste them in. This is because of some security script on shopify
    # that I guess detects sending characters programatically too fast with .send_keys()? idk but this works
    os.system("echo %s| clip" % field_map[iframe_id]['value'])
    driver.find_element_by_id(field_map[iframe_id]['input_id']).send_keys(Keys.CONTROL,"v")

    driver.switch_to.default_content()

driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

print("Credit Card info entered, hitting 'Pay Now'")
print("Total time: " + str(time.time() - start_time))

pay_now_button.click() 
# All done! You should be on the confirmation page.

print("Quitting in 30 seconds...")

time.sleep(30)
driver.quit()


"""
# Returns the url for the product that we're looking for on the shopify powered site if the product is live 
# (Not used since we knew the url of the u80a-seq1 extra posting beforehand, but could be useful if you're expecting a product that hasn't been published yet)
def checkAvailablity():
    r = requests.get('https://ramaworks.store/products.json')
    products = json.loads((r.text))['products']

    for product in products:
        # If you know the exact name of the posting beforehand you can match it like 
        # this: product['title'] == "Name of Posting (Exact)", otherwise try to think of what the name might look like and what
        # other characteristics the posting might have.
        # For example the rama U80-A seq1 extras will definitely have "U80-A" in the title and will definitely not have "Seq2",
        # Since the current preorder for the U80-A Seq2 has its product_type set to "Keyboard" we can assume the listing for the 
        # seq1 extras will also.
        if ("u80-a" in product['title'].lower()) and ("seq2" not in product['title'].lower()) and (product['product_type'] == 'Keyboard'):          
            url = "https://ramaworks.store/products/" + product['handle']
            print(product['title'] + " | " + url )
            return url
    return False
"""