import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions, expected_conditions
from selenium.common.exceptions import *
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_extension('./ngpampappnmepgilojfohadhhmbhlaek.crx') 
options.add_extension('./gighmmpiobklfepjocnamgkkbiglidom.crx') 
browser = webdriver.Chrome('./chromedriver',options=options)
if len(sys.argv)<2:
 fl=input("Enter the name of the file or path:")
else: 
 fl=sys.argv[1]
print("File to be opened: "+fl)
if not os.path.isfile(fl):
    print('File path "{}" does not exist.\n\nExiting...'.format(fl))
    sys.exit()
else:
 file1 = open(fl, 'r')
 count = 0 
 flag  = 0
 dlcount = 0
 x=[]
 line= file1.readline()
 x=[line]
 print("File successfully opened\nProceeding to opening first Link....\n")
 while True: 
     flag+=1
     line2= file1.readline()
     x.append(line2)
     line=x[flag-1]
     if not line.strip() and not line2.strip():
         file1.close()
         print("\n\nReached end of file\n\nTotal Lines Parsed: {}\nTotal Links found: {}\nTotal downloads started: {}\n\nExiting........\n\n".format(flag,count,dlcount))
         break 
         sys.exit()
     elif not line.strip() or line.strip()[0:4] !="http":
         print('No Link found on Line {}:"'.format(flag)+line.strip()+'" it is either Empty or Invalid\nMoving to next line....\n')
         continue	
     else:
      try:	
       browser.get(line)
       count += 1 
       sleep(1)
       print('Link {}: "{}" successfully opened\nProceeding to download file.... '.format(count,line.strip())) 
      except WebDriverException:
          print("Unable to open link\n Moving to next...")
          element = None
          i = 6
          while element is None:
           try:
            wait = WebDriverWait(browser, 5, poll_frequency=1)
            element = wait.until(expected_conditions.visibility_of_element_located("container"))
            continue
           except:
            browser.refresh()
            i = i - 1
            print(i)
            if i < 0:
             raise Exception('Page not loaded')
          sleep(3)  
          browser.execute_script("window.open('');")
          sleep(1)
          browser.switch_to.window(browser.window_handles[count+2])
          continue
      try:
       element = browser.find_element_by_xpath("//*[@id='dlbutton']")
       element.click()
       dlcount+=1
      except NoSuchElementException:
       print("Could not find the download link\nProceeding to next..")
       browser.execute_script("window.open('');")
       sleep(1)
       browser.switch_to.window(browser.window_handles[count+2])
       continue 
      print("Download successfully started for Link{}: {}\nProceeding to next link.....\n ".format(count,line.strip()))    
file1.close()               