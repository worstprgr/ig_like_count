#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
from pathlib import Path
import os
import csv
import time
import sys

# # # # # # # # # # # REQUIREMENTS: # # # # # # # # # #
# - Selenium                                          #
# - Webdriver for Chrome and/or Firefox(Geckodriver)  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # CHECKLIST # # # # # # # # # # # #
# - Line 44/51: Set correct browser engine            #
# - Line 46/53: Set headless to TRUE                  #
# - Line 57: Set correct service                      #
# - Line 62: Set correct webdriver                    #
# - Line 42: Set correct target                       #
# - Line 68: Set scraping duration                    #
# - Line 72: Set path suffix                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

# TODO: Further ideas
#       1. set a custom time, how long the scraping should work - DONE
#       2. exceptions, monitoring and errors - HALF DONE
#       3. credentials and url target inside a .txt?
#       4. hash IG password
#       5. 2FA?
#       6. memory leak?
#       7. saved .csv in drive or in memory?

# login page
url_login = 'https://www.instagram.com/accounts/login/'
# main target
url_scrape = 'https://www.instagram.com/p/Cbx48u1tZvW/'

# # Chrome Options
# chromeOptions = Options()
# chromeOptions.headless = False
# chromeOptions.add_argument("--disable-dev-shm-usage")
# chromeOptions.add_argument("--no-sandbox")
# chromeOptions.add_argument("--window-size=800,800")

# Firefox Options
options = FirefoxOptions()
options.headless = True
options.add_argument("--window-size=800,800")
options.add_argument("--no-sandbox")

# s = Service('/usr/bin/chromedriver')  # LinuxChrome
# s = Service('C:/chromedriver/chromedriver.exe')  # WindowsChrome
s = Service('/usr/bin/geckodriver')  # LinuxFirefox
# s = Service('C:/firefoxdriver/geckodriver.exe')  # WindowsFirefox

# driver = webdriver.Chrome(service=s, options=chromeOptions)
driver = webdriver.Firefox(service=s, options=options)

# length of the script
# 5760 = 96h / 2880 = 48h / 1440 = 24h / 720 = 12h / 360 = 6h / 180 = 3h
epoch = 1  # don't touch
epochs = 1440

# account data
ig_account = "NAME"  # TODO: hash
ig_pwd = "PASS"  # TODO: hash

# path to csv
path_suffix = 'wa_ig2'

datapath = '/scraper/data/' + path_suffix + '/'  # Linux
# datapath = 'data/' + path_suffix + '/'  # Local testing (Windows)

# create path var
path = datapath + path_suffix + '.csv'
print(path)

# lists
header = [
    'DATETIME',
    'COUNT'
]
quantity = []


try:
    Path(datapath).mkdir(parents=True, exist_ok=True)  # if folders don't exist
    Path(path).touch(exist_ok=True)  # if csv don't exists
except PermissionError:
    print('Creating folder and csv-file failed. Check permissions.')
    sys.exit()

# write zeros if file is empty
csv_empty = os.stat(path).st_size == 0

if csv_empty is True:
    with open(path, 'w', encoding='utf8', newline='') as f:
        writeZero = csv.writer(f)
        writeZero.writerow(header)


# failed attempts
c_cookie = 1
c_login = 1
error_count = 3

# IG login
print('###### INSTAGRAM LOGIN #######')
driver.get(url_login)
time.sleep(2)

# cookie clicker
if c_cookie <= error_count:
    try:
        cookie_nope = driver.find_element(By.XPATH, "//button[@class='aOOlW   HoLwm ']")
        cookie_nope.click()
        print('[DRIVER]: 01. Reject Cookies')
        time.sleep(2)
    except:
        print('[ERROR @ LOC - Cookie Clicker]: Connection Error or can not find HTML element. Sleeping 10s ...')
        c_cookie = c_cookie + 1
        time.sleep(10)
else:
    print('[ERROR @ LOC - Cookie Clicker]: Too many errors occurred!')
    sys.exit()


# login
if c_login <= error_count:
    try:
        username_input = driver.find_element(By.XPATH, "//input[@aria-label='Phone number, username, or email']")
        password_input = driver.find_element(By.XPATH, "//input[@aria-label='Password']")
        username_input.send_keys(ig_account)
        password_input.send_keys(ig_pwd)
        print('[DRIVER]: 02. Login')
        time.sleep(4)

        login_button = driver.find_element(By.XPATH, "//button[@class='sqdOP  L3NKy   y3zKF     ']")
        login_button.click()
        print('[DRIVER]: 03. Send it')
        time.sleep(4)
    except:
        print('[ERROR @ LOC - Login]: Connection Error or can not find HTML element. Sleeping 10s ...')
        c_login = c_login + 1
        time.sleep(10)
else:
    print('[ERROR @ LOC - Login]: Too many errors occurred!')
    sys.exit()


# switch to target URL
print('[DRIVER]: 04. Change URL')
driver.get(url_scrape)
time.sleep(2)


# scraper
print("[DRIVER]: 05. Start the big loop!")
# the big loop
while epoch <= epochs:
    # create timestamp
    dateTimeObj = datetime.now()
    dateObj = dateTimeObj.date()
    timeObj = dateTimeObj.time()
    dateStr = dateObj.strftime("%Y-%m-%d")
    timeStr = timeObj.strftime("%H:%M")
    timestamp = [dateStr + ' ' + timeStr]
    CompSec = timeObj.strftime("%S")

    time.sleep(1)
    if CompSec == '00':
        print(str(timestamp) + ' - [' + epoch + '/' + epochs + ']') # TODO: NEW! Check!
        driver.refresh()
        time.sleep(5)
        search2 = driver.find_element(By.XPATH,
                                      '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div['
                                      '2]/section[2]/div/div[2]/div/a/div/span')
        print(int(search2.get_attribute('innerHTML')) + 1)
        quantity = [int(search2.get_attribute('innerHTML')) + int(1)]

        # Write to DB
        data = timestamp + quantity

        with open(path, 'a', encoding='utf8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

        epoch = epoch + 1


print("[DRIVER]: 06. Scraping done! Closing connection.")
driver.quit()
