import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
options = webdriver.ChromeOptions()
options.add_extension('./ngpampappnmepgilojfohadhhmbhlaek.crx') 
options.add_extension('./gighmmpiobklfepjocnamgkkbiglidom.crx') 
browser = webdriver.Chrome('./chromedriver',options=options)
# browser = webdriver.Chrome('./chromedriver')
# fl=input("Enter the name of the file or path:")
fl=sys.argv[1]
print("File to be opened: "+fl)
if not os.path.isfile(fl):
    print("File path {} does not exist. Exiting...".format(fl))
    sys.exit()
else:
 file1 = open(fl, 'r')
 count = 0 
 print("File successfully opened\nProceeding to opening first Link....\n")
 with open(fl) as file1:
      line=file1.readlines()
 for i in line:
        print (i)       
 while True:
     
     # for i in line:
     #    print (i)
     #print(line[0])
     
     # line2= file1.readline()
     # line3=line2
     if not line[count].strip() and not line[count+1].strip():
     	file1.close()
     	print("\n\n\nReached end of file\nExiting........\n\n")
     	break 
     	sys.exit()
     elif not line[count] or line[count].strip()[0:4] !="http":
      continue
     	#print(line[count].strip()[0:4])
     	#print("Empty or Invalid line encountered\nMoving to next line....\n")
     		
     else:
      try:		
       #sleep(1)	
       browser.get(line[count])
       count += 1 
       print("Link {}: {} successfully opened\nProceeding to download file.... ".format(count,line[count-1].strip())) 
      except WebDriverException:
      	print("Unable to open link\n Moving to next...")
      	#sleep(2)
      	browser.execute_script("window.open('');")
      	sleep(1)
      	browser.switch_to.window(browser.window_handles[count])
      	continue
      #element = browser.find_element_by_id("dlbutton")
      try:
       element = browser.find_element_by_xpath("//*[@id='dlbutton']")
       element.click()
      except NoSuchElementException:
       print("Could not find the download link\nProceeding to next..")
       browser.execute_script("window.open('');")
       sleep(1)
       browser.switch_to.window(browser.window_handles[count+2])
       continue 
      print("Download successfully started for Link{}: {}\nProceeding to next link..... ".format(count,line[count-1].strip()))    
file1.close()      

  

