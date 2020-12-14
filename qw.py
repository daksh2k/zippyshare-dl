import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains 
  
# Creating an instance webdriver 
browser = webdriver.Chrome('./chromedriver')

# for i in range(5):
ele=browser.find_element_by_tag_name('body')
ActionChains(browser).move_to_element(ele).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
sleep(1);
ActionChains(browser).move_to_element(ele).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()
sleep(1);
ActionChains(browser).move_to_element(ele).key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()