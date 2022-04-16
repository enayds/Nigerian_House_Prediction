import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


options = Options()

path = ('C:/Users/EGBUNA/chromedriver_win32/chromedriver.exe')
driver = webdriver.Chrome(service = Service(path), options = options)

url = 'https://jiji.ng/abuja/houses-apartments-for-sale'
driver.get(url)

wait = WebDriverWait(driver, 15) # defining the waiting period for the driver
driver.maximize_window() # maximize the window of the browser

driver.implicitly_wait(10)
houses = []
## i need to scroll to the end of the page here so i can get at least 100 houses
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") #scrolling
    list_of_houses = driver.find_elements(By.CSS_SELECTOR, 'div.b-list-advert__item-wrapper')
    if len(list_of_houses) >= 200: ## checking to see if the target number of houses are met
        break
    time.sleep(5)
    
main_list = []
for i in list_of_houses:
    temp_link = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
    main_list.append(temp_link)
number = 0    
for link in main_list:
    driver.execute_script('window.open();') # opening a new empty tab
    driver.switch_to.window(driver.window_handles[1]) # switches focus to the newly opened tab
    driver.get(link)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.qa-advert-price-view-value')))
    driver.execute_script("window.stop();")
    print('stopped')
    try:
        price = driver.find_element(By.CSS_SELECTOR, '.qa-advert-price-view-value').text
    except:
        price = 'none'
    try:
        div = driver.find_element(By.CSS_SELECTOR, '.b-advert-info-statistics__inner') # getting the info div

        info = div.find_elements(By.TAG_NAME, 'div') # getting all presents divs in the info div
        new_info = [f.text for f in info] # collecting the text from each div and storing in new_info variable

        location = new_info[2]     # collecting the location div
    except:
        location ='none'
    try:
        rent_duration = driver.find_element(By.CSS_SELECTOR, '.b-alt-advert-price__period').text
    except NoSuchElementException:
        rent_duration = 'anually'
    att = driver.find_elements(By.CSS_SELECTOR, 'div.b-advert-icon-attribute')
    house_type = att[0].text
    rooms = att[1].text
    bathrooms = att[2].text
    
    oth = driver.find_elements(By.CSS_SELECTOR, 'div.b-advert-attribute')
    temp_dict = {
        'price':price,
        'location': location,
        'house_type': house_type,
        'rooms': rooms,
        'bathrooms':bathrooms,
        'rent_duration': rent_duration
        }
    for i in oth:
        temp_link = i.text
        temp_dict[temp_link.split('\n')[-1]] = temp_link.split('\n')[0]
    
    number += 1
    print('number of house data collected = ', number)
    houses.append(temp_dict)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
driver.quit()