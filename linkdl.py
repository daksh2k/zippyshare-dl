import os
import sys
from time import sleep
from os import system
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import *
print("\n\n\n\n")
system('cls')
if len(sys.argv)<2:
 fl=input("Enter the name of the file or path:")
else: 
 fl=sys.argv[1]
if not os.path.isfile(fl):
    print('\nFile path "{}" does not exist.\nExiting...\n\n'.format(fl))
    sys.exit()
else:	
 start_time = datetime.now()
 dt_string = start_time.strftime("%d/%m/%Y %H:%M:%S")
 print("\n\nProcess started on Date and Time =", dt_string)
 print("\n\nFile to be opened: "+fl)		
 options = webdriver.ChromeOptions()
 options.add_argument('--ignore-certificate-errors')
 options.add_argument('--ignore-ssl-errors')
 options.add_extension('./Selenium/Extensions/ngpampappnmepgilojfohadhhmbhlaek.crx') 
 options.add_extension('./Selenium/Extensions/gighmmpiobklfepjocnamgkkbiglidom.crx') 
 # options.add_experimental_option("debuggerAddress", "localhost:3000")
 print("\n\nAdding Extensions to browser..\nThis process will take a few seconds...\n")
 browser = webdriver.Chrome('./Selenium/chromedriver',options=options)
 print('\nBrowser successfully opened\nOpening file "'+fl+ '" to read links...\n\n')
 file1 = open(fl, 'r')
 count = 0 
 flag  = 0
 dlcount = 0
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
         end_time = datetime.now()
         dt_string = end_time.strftime("%d/%m/%Y %H:%M:%S")
         print("\n\nReached end of file\n\nTotal Lines Parsed: {}\nTotal Links found: {}\nTotal downloads started: {}\n\nExiting........\n\n".format(flag,count,dlcount))
         print("Process ended on Date and Time =", dt_string)
         print("\n\n\n\n")
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
       print('Link {}: "{}" found on Line {}.\nLink successfully opened.\nProceeding to download file.... '.format(count,line.strip(),flag)) 
      except WebDriverException:
          print("Unable to open link\n Moving to next...")
          sleep(3)
          browser.refresh()  
          browser.execute_script("window.open('');")
          sleep(1)
          browser.switch_to.window(browser.window_handles[count+2])
          continue
      try:
       element = browser.find_element_by_xpath("//*[@id='dlbutton']")
       element.click()
       dlcount+=1
      except NoSuchElementException:
       print("Could not find the download link\nProceeding to next..\n\n")
       browser.execute_script("window.open('');")
       sleep(1)
       browser.switch_to.window(browser.window_handles[count+2])
       continue 
      print("Download successfully started for Link{}: {}\nProceeding to next link.....\n ".format(count,line.strip()))    
file1.close()   