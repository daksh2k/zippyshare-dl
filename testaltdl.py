import os
import sys
from time import sleep,time
from os import system, remove
from dcryptit import read_dlc
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import *
link_count = 0 
tab_count = 0
lines_parsed  = 0
dlcount = 0
flcount = 0
total_lines_parsed = 0
system('cls')
exec_time = datetime.now().strftime("%d_%m__%H_%M_%S") 
start_time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
exec_start_time=time()
print("Process started on Date and Time =", start_time)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('user-data-dir=D:/College/Projects/zippyshare-dl/Selenium/Chrome_Test_Profile') 
# options.add_argument("--headless")
# options.add_experimental_option("debuggerAddress", "localhost:4000")
print("\n\nOpening browser\nThis process will take a few seconds...\n")
browser = webdriver.Chrome('./Selenium/chromedriver',options=options)
print("\nBrowser successfully opened...")
file_list=[]
if len(sys.argv)<2:
 file_inputs=input("Enter the name of the file or path(if multiple separete by commas):")
 for file in file_inputs.strip().split(','):
      file_list.append(file.strip())
else: 
 for i in range(1,len(sys.argv)):
  file_list.append(sys.argv[i])
print(f"\n\nTotal files to be opened: {len(file_list)}")
file_list_base = list(map(lambda fl : os.path.basename(fl), file_list))
file_string_list = ", ".join(file_list_base)
print("Files to be opened: "+file_string_list)
for fl in file_list:
  flcount+=1
  if not os.path.isfile(fl):
    print(f'\nFile path "{fl}" does not exist.\nExiting...\n\n')
    # input("Press any key to exit")
    sys.exit()
  else:
   # chrome_run = os.system('"chrome.exe -remote-debugging-port=4000 --user-data-dir="D:/College/Projects/zippyshare-dl/Selenium/Chrome_Test_Profile"') 
   # print(f"this is chrom run {chrome_run}")
   # exec_time = datetime.now().strftime("%d_%m__%H_%M_%S") 
   # start_time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
   # exec_start_time=time()
   # print("\n\nProcess started on Date and Time =", start_time)
   print(f'\nOpening File {flcount} of {len(file_list)}: "{os.path.basename(fl)}"\nLocated at: "{os.path.realpath(fl)}"\n')    
   # options = webdriver.ChromeOptions()
   # options.add_argument('--ignore-certificate-errors')
   # options.add_argument('--ignore-ssl-errors')
   # options.add_argument("--no-sandbox")
   # options.add_argument("--headless")
   # options.add_argument("disable-gpu")
   # options.add_extension('./Selenium/Extensions/ngpampappnmepgilojfohadhhmbhlaek.crx') 
   # options.add_extension('./Selenium/Extensions/gighmmpiobklfepjocnamgkkbiglidom.crx') 
   # options.add_experimental_option("debuggerAddress", "localhost:4000")
   # print("\n\nConnecting with browser\nThis process will take a few seconds...\n")
   # browser = webdriver.Chrome('./Selenium/chromedriver',options=options)
   # print('\nOpening file "'+os.path.basename(fl)+ '" to read links...\n\n')
   zipp_link = False
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
   
   line= file1.readline()
   x=[line]
   print("File successfully opened\nProceeding to opening first Link....\n")
   lines_parsed=0
   while True:
       lines_parsed+=1
       line2= file1.readline()
       x.append(line2)
       line=x[lines_parsed-1]
       if not line.strip() and not line2.strip():
           file1.close()
           if(zipp_link):
            file2.close()
           if fl.lower().endswith('.dlc'):
            remove(temp_file)
           total_lines_parsed+=lines_parsed
           if(zipp_link):
            print(f'\n\nDownload Links saved to file "{dl_Links}"\nLocated at "{os.path.realpath(dl_Links)}"')
           if(flcount!=len(file_list)):
            print(f'\nFile: "{os.path.basename(fl)}" successfully parsed!\nMoving to next file...')
            print("\n######################################################################################################")
           if(flcount==len(file_list)):
            end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            exec_end_time=time()
            duration= exec_end_time- exec_start_time
            hours, rest = divmod(duration,3600)
            minutes, seconds = divmod(rest, 60)
            print(f"\n\nTotal Links found: {link_count}\nTotal downloads started: {dlcount}\nTotal files parsed for Links: {flcount}\nTotal Lines Parsed: {total_lines_parsed}")
            print(f"Total time taken: {str(hours).split('.')[0]} Hours {str(minutes).split('.')[0]} Minutes {str(seconds).split('.')[0]} Seconds\n\nExiting........\n\n")
            print("Process ended on Date and Time =", end_time)
            print("\n\n\n\n")
           # if(zipp_link):
            # os.system(f"subl {dl_Links}")
            # os.system('"C:/Program Files (x86)/Internet Download Manager/IDMan.exe"')
            # break 
           # sys.exit()
           break
       elif not line.strip() or line.strip()[0:4] !="http":
           print(f'No Link found on Line {lines_parsed}:"'+line.strip()+'" it is either Empty or Invalid\nMoving to next line....\n')
           continue 
       else:
        try:  
         browser.get(line)
         link_count += 1 
         print(f'Link {link_count}: "{line.strip()}" found on Line {lines_parsed}.\nLink successfully opened.\nProceeding to download file.... ') 
        except WebDriverException:
            tab_count+=1
            print("Unable to open link\nMoving to next...")
            sleep(3)
            browser.refresh()  
            sleep(3)
            browser.execute_script("window.open('');")
            sleep(0.5)
            browser.switch_to.window(browser.window_handles[tab_count-1])
            continue
        try:
         if(line.find('zippy')!=-1):
          element = browser.find_element_by_xpath("//*[@id='dlbutton']").get_attribute("href");
          size= len(fl) 
          mod_string = fl[:size - 4] 
          orig_name=os.path.basename(mod_string)
          dl_Links="{}_dl_links.txt".format(orig_name)
          file2 = open(dl_Links, "a") 
          file2.write(element+"\n")
          dlcount+=1 
          zipp_link = True 
         elif(line.find('sharer')!=-1): 
          tab_count+=1
          element = browser.find_element_by_xpath("//*[@id='btndl']")
          browser.find_element_by_xpath("//*[@id='overlay']").click()
          sleep(0.5)
          element.click()
          browser.execute_script("window.open('');")
          sleep(0.5)
          browser.switch_to.window(browser.window_handles[tab_count])
          dlcount+=1
         else:
          raise NoSuchElementException 
        except NoSuchElementException:
         tab_count+=1 
         print("Could not find the download link\nProceeding to next..\n\n")
         browser.execute_script("window.open('');")
         sleep(0.5)
         browser.switch_to.window(browser.window_handles[tab_count])
         continue 
        print(f"Download successfully started for Link {link_count}: {line.strip()}\nProceeding to next link.....\n")    
  file1.close()     