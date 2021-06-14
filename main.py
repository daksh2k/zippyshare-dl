import os
import sys
import re
import requests
from time import sleep,time
from os import system, remove
from dcryptit import read_dlc
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import *

# Summary vars initialization
link_count = 0 
tab_count = 0
lines_parsed  = 0
dlcount = 0
flcount = 0
flcount_parsed = 0
total_lines_parsed = 0
filecrypt_domain = "https://www.filecrypt.cc/"
start_time  = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
exec_start_time=time()

def parse_filecrypt():  
  for index,item in enumerate(file_list):
    global tab_count
    # print(f"\nLink {item}\n")
    if(item.find('filecrypt')!=-1):
      print(f"\nFound filecrypt Link: {item}\nGetting dlc from filecrypt..")
      try:
       browser.get(item)
       try:
       	dlc_id = browser.find_element_by_class_name("dlcdownload").get_attribute("onclick")
        dlc_name = browser.find_element_by_tag_name("h2").get_attribute("textContent") 
        print("DLC name: ",dlc_name)
        link_to_download = filecrypt_domain + "DLC/" + dlc_id.split("'")[1]+ ".dlc"
        file_path = "Links/"+dlc_name+".dlc"
        if os.path.isfile(file_path):
         if os.path.getsize(file_path)==0:
             print("File exists but with size 0\n Deleteing File and Downloading Again")
             remove(file_path)
         else:
           file_list[index] = file_path
           print(f"{file_path} already exists\n\tSkipping Download...")
           if(index+1==len(file_list)):
             break
           else:
             print("\t\tMoving to next file...\n")
             continue 
        r = requests.get(link_to_download)
        open(file_path, 'wb').write(r.content)
        file_list[index] = file_path
       except: 
       	raise ValueError('\nUnable to find DLC \n%s is not supported. Try opening the link manually.' % item)
        if(index+1==len(file_list)):
         break
        else:
         print("Moving to next item...")
         tab_count+=1 
         browser.execute_script("window.open('');")
         sleep(0.5)
         browser.switch_to.window(browser.window_handles[tab_count])
         continue
      except Exception as e:
        print('[*] {}'.format(e))
        if(index+1==len(file_list)):
            break
        else:
            print("Moving to next item...")
            tab_count+=1 
            browser.execute_script("window.open('');")
            sleep(0.5)
            browser.switch_to.window(browser.window_handles[tab_count])
            continue 
            # Alternate pattern r"(https?:\/\/)?(\w*\.)?(\w+)\.(.+)"
    elif(re.match(r"https?:\/\/(\w*\.)?(\w+)\.(.+)",item) is not None and item.find('filecrypt')==-1):
      patt = "Links/"+re.findall(r"https?://(\w*\.)?(\w+)\..+",item)[0][1]+datetime.now().strftime("_%d_%m_%y")+".txt"
      lfl = open(patt,'a')
      print(f"\nLink: {item} saved to file {patt}")
      lfl.write("\n"+item+"\n")
      lfl.close()
      file_list[index] = patt 

def display_summary():
  end_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  exec_end_time=time()
  duration= exec_end_time- exec_start_time
  hours, rest = divmod(duration,3600)
  minutes, seconds = divmod(rest, 60)
  print("\n############################  Summary   ##################################################")
  print(f"\nTotal Links found: {link_count}\nTotal downloads started: {dlcount}\nTotal files parsed for Links: {flcount_parsed}/{flcount}\nTotal Lines Parsed: {total_lines_parsed}")
  print(f"Total time taken: {str(hours).split('.')[0]} Hours {str(minutes).split('.')[0]} Minutes {str(seconds).split('.')[0]} Seconds\n\nExiting........\n\n")
  print("Process ended on Date and Time =", end_time)
  print("\n\n\n\n")

system('cls')
print("Process started on Date and Time =", start_time)
cwd = os.getcwd()
print("Current working directory: {0}\n".format(cwd))
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('user-data-dir='+cwd+'\\Selenium\\Chrome_Test_Profile')  
# options.add_argument("--headless")
# options.add_experimental_option("debuggerAddress", "localhost:4000")
print("\nOpening browser\nThis process will take a few seconds...\n")
try:
  browser = webdriver.Chrome('./Selenium/chromedriver',options=options)
except Exception as e:
        print('[*] {}'.format(e))
        browser = webdriver.Chrome('./Selenium/chromedriver')
print("Browser successfully opened...")
if not os.path.exists('Links'):
      print("Creating Folder Links to store download Links....\n")
      os.makedirs('Links')
file_list=[]
if len(sys.argv)<2:
 file_inputs=input("\nEnter the name of the file or path(if multiple separete by commas): ")
 for file in file_inputs.strip().split(','):
      file_list.append(file.strip())
else: 
 for i in range(1,len(sys.argv)):
  file_list.append(sys.argv[i])
  
parse_filecrypt()
print(f"\n\nTotal files to be opened: {len(file_list)}")
file_list_base = list(map(lambda fl : os.path.basename(fl), file_list))
file_string_list = ", ".join(file_list_base)
print("Files to be opened: "+file_string_list)
for fl in file_list:
  flcount+=1
  if not os.path.isfile(fl):
   if(flcount==len(file_list)):
    print(f'\nFile path "{fl}" does not exist.')
    display_summary()
    sys.exit()
   else:
    print(f'\nFile path "{fl}" does not exist.\nMoving to next file...')
    print("\n######################################################################################################")
    continue 
  else:
   flcount_parsed+=1
   file_skipped= True
   zipp_link = False
   pixel_link = False
   url_list=[]
   print(f'\nOpening File {flcount} of {len(file_list)}: "{os.path.basename(fl)}"\nLocated at: "{os.path.realpath(fl)}"\n')    
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
   print("\tFile successfully opened\n\t\tProceeding to opening first Link....\n")
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
           if(pixel_link):
            file3.close()
           if fl.lower().endswith('.dlc'):
            remove(temp_file)
           total_lines_parsed+=lines_parsed
           if(zipp_link):
            print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
           if(pixel_link):
            print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
           if(flcount!=len(file_list)):
            print(f'\nFile: "{os.path.basename(fl)}" successfully parsed!\nMoving to next file...')
            print("\n######################################################################################################")
           if(flcount==len(file_list)):
             display_summary()
             sys.exit()
           break
       elif not line.strip() or line.strip()[0:4] !="http":
           print(f'No Link found on Line {lines_parsed}:"'+line.strip()+'" it is either Empty or Invalid\n\tMoving to next line....\n')
           continue 
       else:
        try:  
         try:
          if(line.find('zippy')!=-1):
           size= len(fl) 
           mod_string = fl[:size - 4] 
           orig_name=os.path.basename(mod_string)
           dl_Links="Links/{}_dl_links.txt".format(orig_name)
           if os.path.isfile(dl_Links) and file_skipped:
             if os.path.getsize(dl_Links)==0:
               print("File exists but with size 0\n Deleteing File and Downloading Again")
               remove(dl_Links)
             else:
               skip = input(f"\n\nDl_Links File {dl_Links} already exists.\nDo you want to skip downloading?(Y/N):  ")
               if(flcount==len(file_list) and skip.upper()=="Y"):
                 file_skipped = True
                 # link_count-=1
                 print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
                 if fl.lower().endswith('.dlc'):
                  file.close()	
                  remove(temp_file)
                 display_summary()
                 sys.exit()
               elif(flcount!=len(file_list) and skip.upper()=="Y"):
                 file_skipped = True
                 if fl.lower().endswith('.dlc'):
                  file1.close()
                  remove(temp_file)
                 print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
                 print(f"\nSkipping file {os.path.basename(fl)} \nMoving to next file....")
                 print("\n######################################################################################################")
                 break  
               else:
                 file_skipped = False
                 remove(dl_Links)
                 print("Downloading Links again") 
           file2 = open(dl_Links, "a")
           browser.get(line)
           file_skipped = False
           link_count += 1 
           print(f'Link {link_count}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ') 
           # element2 = browser.find_element_by_xpath("//*[@id='dlbutton']")
           # element2.click()
           element = browser.find_element_by_xpath("//*[@id='dlbutton']").get_attribute("href"); 
           file2.write(element+"\n")

           dlcount+=1 
           zipp_link = True 
          elif(line.find('pixeldrain')!=-1):
           size= len(fl) 
           mod_string = fl[:size - 4] 
           orig_name=os.path.basename(mod_string)
           dl_Links="Links/{}_dl_links.txt".format(orig_name)
           if os.path.isfile(dl_Links) and file_skipped:
             if os.path.getsize(dl_Links)==0:
               print("File exists but with size 0\n Deleteing File and Downloading Again")
               remove(dl_Links)
             else:
               skip = input(f"\n\nDl_Links File {dl_Links} already exists.\nDo you want to skip downloading?(Y/N):  ")
               if(flcount==len(file_list) and skip.upper()=="Y"):
                 file_skipped = True
                 # link_count-=1
                 print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
                 if fl.lower().endswith('.dlc'):
                  file1.close()	
                  remove(temp_file)
                 display_summary()
                 sys.exit()
               elif(flcount!=len(file_list) and skip.upper()=="Y"):
                 file_skipped = True
                 if fl.lower().endswith('.dlc'):
                  file1.close()	
                  remove(temp_file)
                 print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
                 print(f"\nSkipping file {os.path.basename(fl)} \nMoving to next file....")
                 print("\n######################################################################################################")
                 break  
               else:
                 file_skipped = False
                 print("Downloading Links again") 
           file3 = open(dl_Links, "a")
           # browser.get(line)
           file_skipped = False
           link_count += 1 
           print(f'Link {link_count}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ') 
           # element = browser.find_element_by_xpath("//*[@id='dlbutton']").get_attribute("href");
           element = "https://pixeldrain.com/api/file/"+line.split('/')[4]+"?download"
           file3.write(element+"\n")
           dlcount+=1 
           pixel_link = True 
          elif(line.find('sharer')!=-1): 
           link_count += 1 
           browser.get(line)
           print(f'Link {link_count}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ') 
           element = browser.find_element_by_xpath("//*[@id='btndl']")
           browser.find_element_by_xpath("//*[@id='overlay']").click()
           tab_count+=1
           sleep(0.5)
           element.click()
           browser.execute_script("window.open('');")
           sleep(0.5)
           browser.switch_to.window(browser.window_handles[tab_count])
           dlcount+=1
          elif(line.find('drive')!=-1):
           tab_count+=1
           if(line.find('uc?')!=-1):
            modified_drive_link = line.replace("uc?","open?") 
            browser.get(modified_drive_link)
            link_count += 1 
            print(f'Link {link_count}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ') 
           print("Could not find the download link\n\tProceeding to next..\n\n")
           browser.execute_script("window.open('');")
           sleep(0.5)
           browser.switch_to.window(browser.window_handles[tab_count])
           continue 
          else:
           browser.get(line)
           link_count += 1 
           print(f'Link {link_count}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ')
           raise NoSuchElementException 
         except NoSuchElementException:
          tab_count+=1 
          print("Could not find the download link\n\tProceeding to next..\n\n")
          browser.execute_script("window.open('');")
          sleep(0.5)
          browser.switch_to.window(browser.window_handles[tab_count])
          continue 
         print(f"\nDownload successfully started for Link {link_count}: {line.strip()}\n\tProceeding to next link.....\n")
        except WebDriverException:
            tab_count+=1
            print(f"Unable to open Link: {line.strip()}\n")
            for i in range(5):
             sleep(0.5)
             browser.refresh()
             print(f"Refreshing page...\tRetry: {i+1}",end="\r")
             if(i==4):
              print(f"\n\nMoving to next Link...\tRetried count: {i+1}\n")    
            sleep(0.5)
            browser.execute_script("window.open('https://www.google.com','_blank');")
            sleep(0.5)
            browser.switch_to.window(browser.window_handles[tab_count])
            continue
  file1.close()     