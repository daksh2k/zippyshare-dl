import os
import sys
from time import sleep,time
from os import system
from os import remove
from dcryptit import read_dlc
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
 start_time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
 exec_start_time=time()
 print("\n\nProcess started on Date and Time =", start_time)
 print(f'\n\nFile to be opened: "{os.path.basename(fl)}"\nLocated at: "{os.path.realpath(fl)}"')       
 options = webdriver.ChromeOptions()
 options.add_argument('--ignore-certificate-errors')
 options.add_argument('--ignore-ssl-errors')
 options.add_extension('./Selenium/Extensions/ngpampappnmepgilojfohadhhmbhlaek.crx') 
 options.add_extension('./Selenium/Extensions/gighmmpiobklfepjocnamgkkbiglidom.crx') 
#  options.add_experimental_option("debuggerAddress", "localhost:4000")
 print("\n\nConnecting with browser\nThis process will take a few seconds...\n")
 browser = webdriver.Chrome('./Selenium/chromedriver',options=options)
 print('\nBrowser successfully connected\nOpening file "'+os.path.basename(fl)+ '" to read links...\n\n')
 url_list=[]
 if fl.lower().endswith('.txt'):
  print("Reading from text file...")
  file1 = open(fl, 'r')
 elif fl.lower().endswith('.dlc'):
  print("Reading from dlc file...")
  url_list += read_dlc(path=fl)
  temp_time = datetime.now().strftime("%d_%m__%H_%M_%S")
  temp_file="temp_{}.txt".format(temp_time)
  file1 = open(temp_file, "w")
  for url in list(url_list): 
   file1.write(url+"\n")
  file1.close()
  file1 = open(temp_file, 'r')  
 count = 0 
 flag  = 0
 dlcount = 0
 line= file1.readline()
 x=[line]
 print("File successfully opened\nProceeding to opening first Link....\n")
 while True:
     # if dlcount==0:
     #  print("Starting...\n\n")
     # elif dlcount%10==0:
     # print("Started {} downloads pausing for 5 mins...\n\n".format(dlcount))	
     #  sleep(300)  
     flag+=1
     line2= file1.readline()
     x.append(line2)
     line=x[flag-1]
     if not line.strip() and not line2.strip():
         file1.close()
         if fl.lower().endswith('.dlc'):
          remove(temp_file)
         end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
         exec_end_time=time()
         duration= exec_end_time- exec_start_time
         hours, rest = divmod(duration,3600)
         minutes, seconds = divmod(rest, 60)
         print("\n\nReached end of file\n\nTotal Lines Parsed: {}\nTotal Links found: {}\nTotal downloads started: {}\nTotal time taken = {} Hours {} Minutes {} Seconds\n\nExiting........\n\n".format(flag,count,dlcount,str(hours).split('.')[0],str(minutes).split('.')[0],str(seconds).split('.')[0]))
         print("Process ended on Date and Time =", end_time)
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
       print('Link {}: "{}" found on Line {}.\nLink successfully opened.\nProceeding to download file.... '.format(count,line.strip(),flag)) 
      except WebDriverException:
          print("Unable to open link\n Moving to next...")
          sleep(3)
          browser.refresh()  
          sleep(3)
          browser.execute_script("window.open('');")
          sleep(0.5)
          browser.switch_to.window(browser.window_handles[count-1])
          continue
      try:
       if(line.find('zippy')!=-1):
        element = browser.find_element_by_xpath("//*[@id='dlbutton']")
        element.click()
        # browser.execute_script("window.open('');")
        # sleep(0.5)
        # browser.switch_to.window(browser.window_handles[count])
        dlcount+=1  
       elif(line.find('sharer')!=-1): 
        element = browser.find_element_by_xpath("//*[@id='btndl']")
        browser.find_element_by_xpath("//*[@id='overlay']").click()
        sleep(0.5)
        element.click()
        browser.execute_script("window.open('');")
        sleep(0.5)
        browser.switch_to.window(browser.window_handles[count])
        dlcount+=1
       else:
        raise NoSuchElementException 
      except NoSuchElementException:
       print("Could not find the download link\nProceeding to next..\n\n")
       browser.execute_script("window.open('');")
       sleep(0.5)
       browser.switch_to.window(browser.window_handles[count])
       continue 
      print("Download successfully started for Link {}: {}\nProceeding to next link.....\n ".format(count,line.strip()))    
file1.close()   