# -*- coding:utf8 -*-
from selenium import webdriver
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='dzy.log',
                    filemode='a')
sleep_time = 1703
option = webdriver.ChromeOptions()
option.add_argument('--headless')
for dd in range(18):
    start = time.time()
    logging.info("")
    print()
    logging.info("Begin %d Loop" % dd)
    print("Begin %d Loop" % dd)
    driver = webdriver.Chrome(chrome_options=option)
    driver.get(
        '''http://10.90.128.10/ssoserver/login/welcome?service=http%3A%2F%2F10.90.90.90%3A8080%2FredirctPortal''')
    #driver.minimize_window()
    logging.info("Scrap Web & Waiting for 10s")
    print("Scrap Web & Waiting for 10s")
    time.sleep(10)
    elem_user = driver.find_element_by_xpath('''//*[@id="username"]''')
    elem_user.send_keys('sunbo')
    elem_pwd = driver.find_element_by_xpath('''//*[@id="pwd"]''')
    elem_pwd.send_keys('SUNseanBO8.')

    commit = driver.find_element_by_xpath('''//*[@id="login"]''')
    commit.click()
    logging.info("Wait for Login & Waiting for 1min")
    print("Wait for Login & Waiting for 1min")
    time.sleep(60)
    nav = driver.find_element_by_xpath('''//*[@id="header"]/div[2]/div[3]''')
    nav.click()
    logout = driver.find_element_by_xpath('''//*[@id="userNav"]/ul/li[8]/a''')
    logging.info("Wait for Logout & Waiting for %d min" % (sleep_time / 60))
    print("Wait for Logout & Waiting for %d min" % (sleep_time / 60))
    logging.info("Sleeping......")
    print("Sleeping......")
    #time.sleep(1)
    time.sleep(sleep_time)
    sleep_time = sleep_time + 118
    logout.click()
    logging.info("Wait for Quit & Waiting for 1s")
    print("Wait for Quit & Waiting for 1s")
    time.sleep(1)
    driver.quit()
    end = time.time()
    logging.info("Time used: %f min" % ((end - start) / 60))
    print("Time used: %f min" % ((end - start) / 60))
    logging.info("Finish %d Loop" % dd)
    print("Finish %d Loop" % dd)

