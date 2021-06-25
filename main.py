import os
import sys
import re
import requests
from time import sleep,time
from os import remove,system
from dcryptit import read_dlc
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from colorama import Fore,init
init(autoreset=True)

#CONFIG VARS
ADD_EXTENSIONS = 1      # Add Adblocker and IDM Extension to the Browser Instance
DEBUG_ADDRESS = 0       # Connect to already Running Browser on a debug port
START_DOWNLOADING = 0   # Start Downloading from Links Directly or just save in a text file.
DIR_CHECK = 1           #If you Want to Auto Add files 
RETRY_COUNT = 3         #Retry If unable to Open Link Min value=1 
DIRS_TO_CHECK = ['.','./Links',os.path.expanduser("~")+"\\Downloads"] # Following Dirs to automatically check for dlc and text files.
COMMON_NAMES = ["requirements.txt","req.txt","requirement.txt"]       #Common Names to Ignore from Directory  
FILECRYPT_DOMAIN = "https://www.filecrypt.cc/"

# Summary vars initialization
link_count = 0 
link_count_tot = 0
tab_count = 0
lines_parsed  = 0
dlcount = 0
flcount = 0
flcount_parsed = 0
total_lines_parsed = 0
file_list=[]
file_list_temp=[]
start_time  = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
exec_start_time=time()

#Get dlc from Filecrypt Links
def parse_filecrypt():  
   for index,item in enumerate(file_list):
      if(item.find('filecrypt')!=-1):
           print(f"\nFound filecrypt Link: {item}\nGetting dlc from filecrypt..")
           try:
               browser.get(item)
               try:
                   dlc_id = browser.find_element_by_class_name("dlcdownload").get_attribute("onclick")
                   dlc_name = browser.find_element_by_tag_name("h2").get_attribute("textContent") 
                   print(Fore.CYAN+f"DLC name: {dlc_name}")
                   link_to_download = FILECRYPT_DOMAIN + "DLC/" + dlc_id.split("'")[1]+ ".dlc"
                   file_path = "Links/"+dlc_name+".dlc"
                   if os.path.isfile(file_path):
                      if os.path.getsize(file_path)==0:
                          print(Fore.YELLOW+"File exists but with size 0\n Deleteing File and Downloading Again")
                          remove(file_path)
                      else:
                          file_list[index] = file_path
                          print(Fore.YELLOW+f"{file_path} already exists\n\tSkipping Download...")
                          if(index+1==len(file_list)):
                              break
                          else:
                              print("\t\tMoving to next file...\n")
                              continue 
                   r = requests.get(link_to_download)
                   open(file_path, 'wb').write(r.content)
                   file_list[index] = file_path
               except Exception as e: 
               	   print(Fore.RED+f"\nUnable to find DLC \n{item} is not supported. Try opening the link manually.")
                   if(index+1==len(file_list)):
                      break
                   else:
                      tab_count = open_newtab(tab_count)
                      continue
           except Exception as e:
                print(Fore.RED+f"[*] {e}")
                if(index+1==len(file_list)):
                    break
                else:
                    tab_count = open_newtab(tab_count)
                    continue 
                 # Alternate pattern r"(https?:\/\/)?(\w*\.)?(\w+)\.(.+)"
      elif(re.match(r"https?\:\/\/(\w*\.)?(\w+)\.(.+)",item) is not None and item.find('filecrypt')==-1):
           patt = "Links/"+re.findall(r"https?\:\/\/(\w*\.)?(\w+)\..+",item)[0][1]+datetime.now().strftime("_%d_%m_%y_%H%M")+".txt"
           lfl = open(patt,'a')
           print(f"\nLink: {item} saved to file {patt}")
           lfl.write("\n"+item+"\n")
           lfl.close()
           file_list[index] = patt 

#Open new Tab in the browser
def open_newtab(tab_count,silent=False,script="window.open('');"):
   if not silent:
      print("Moving to next item...")
   tab_count+=1 
   if tab_count == len(browser.window_handles):
       browser.execute_script(script)
   sleep(0.1)
   browser.switch_to.window(browser.window_handles[tab_count])
   return tab_count

#Check if file already exists in system  
def check_dup(dl_links,file_skipped):
   if os.path.isfile(dl_Links) and file_skipped:
       if os.path.getsize(dl_Links)==0:
           print(Fore.YELLOW+"File exists but with size 0\n Deleteing File and Downloading Again")
           remove(dl_Links)
       else:
          skip = input(f"\n\nDl_Links File {dl_Links} already exists.\nDo you want to skip downloading?(Y/N):  ")
          if(flcount==len(file_list) and skip.upper()=="Y"):
               file_skipped = True
               print(Fore.GREEN+f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
               file1.close()	
               if fl.lower().endswith('.dlc'):
                  remove(temp_file)
               display_summary()
               sys.exit()
          elif(flcount!=len(file_list) and skip.upper()=="Y"):
               file_skipped = True
               file1.close()
               if fl.lower().endswith('.dlc'):
                  remove(temp_file)
               print(Fore.GREEN+f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
               print(f"\nSkipping file {os.path.basename(fl)} \nMoving to next file....")
               print("\n######################################################################################################")
               return 0
          else:
               file_skipped = False
               print("\nDownloading Links again...\n") 
               remove(dl_Links)

#Print the relevant statistics after completion.       
def display_summary():
   hours, rest = divmod(time() - exec_start_time,3600)
   minutes, seconds = divmod(rest, 60)
   print("\n############################  Summary   ##################################################")
   print(f"\nTotal Links found: {link_count_tot}\nLinks successfully opened: {link_count}\nTotal downloads started: {dlcount}\nTotal files parsed for Links: {flcount_parsed}/{flcount}\nTotal Lines Parsed: {total_lines_parsed}")
   print(f"Total time taken: {str(minutes).split('.')[0]} {'Minute' if 1<=minutes<2 else 'Minutes'} {str(seconds).split('.')[0]} Seconds\n\nExiting........\n\n")
   print(f"Process ended on Date and Time: {datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')}\n\n")

system("cls")
print(f"Process started on Date and Time: {start_time}")
cwd = os.getcwd()
print(f"Current working directory: {cwd}\n")

# Check if Chrome Driver is Updated or not 
import check_cdriver.Check_Chromedriver as ccheck 
ccheck.driver_mother_path = "./Selenium"
ccheck.main()

options = webdriver.ChromeOptions()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--allow-insecure-localhost')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('user-data-dir='+cwd+'\\Selenium\\Chrome_Test_Profile') 
if ADD_EXTENSIONS:
    options.add_extension('./Selenium/Extensions/ublock.crx')
    options.add_extension('./Selenium/Extensions/idm.crx')
if DEBUG_ADDRESS:
    options.add_experimental_option("debuggerAddress", "localhost:4000")
caps = DesiredCapabilities.CHROME
caps['acceptInsecureCerts']= True
print("\nOpening browser\nThis process will take a few seconds...\n")

#Connecting with WebDriver
try:
    browser = webdriver.Chrome('./Selenium/chromedriver',options=options,desired_capabilities=caps)
except Exception as e:
    print(Fore.RED+f"[*] {e}")
    browser = webdriver.Chrome('./Selenium/chromedriver',desired_capabilities=caps)
print("Browser successfully opened...")
browser_len = len(browser.window_handles) #fetching the Number of Opened tabs
if browser_len > 1: 
      browser.switch_to.window(browser.window_handles[0]) # Switching the browser focus to First tab.

#Creating Folder links to store the files
if not os.path.exists('Links'):
      print("Creating Folder Links to store download Links....\n")
      os.makedirs('Links')

#Parse Input fron Arguments or By taking Input
if len(sys.argv)<2:
    file_inputs=input("\nEnter the name of the file or path(if multiple separete by commas): ")
    for file in file_inputs.strip().split(','):
        file_list.append(file.strip())
else: 
    for i in range(1,len(sys.argv)):
        file_list.append(sys.argv[i])

#Automatically Add Files from Certain Directories
if DIR_CHECK:
     DIRS_TO_CHECK = list(set(list(map(os.path.realpath,DIRS_TO_CHECK))))
     for dirParse in DIRS_TO_CHECK:
         for entry in os.scandir(dirParse):
             full_p = os.path.join(os.path.realpath(dirParse), entry.name)
             if entry.is_file() and entry.name not in COMMON_NAMES and os.path.splitext(entry.name)[1].lower() in (".txt", ".dlc") and (exec_start_time - os.path.getctime(full_p))/3600 < 24:
                 file_list_temp.append(full_p) 
     if len(file_list_temp)>0:
         dirs_to_check_s = '\n\t\t'.join(DIRS_TO_CHECK)
         print("\nGetting \".dlc\" and \".txt\" files from: \n\t\t"+Fore.YELLOW+dirs_to_check_s+Fore.RESET+"\n")
         print("Following files(Created within last 24 hours) can be added to the File list: \t")
         for ele in file_list_temp:
              print(Fore.CYAN+f"\t\t{os.path.basename(ele)}")           
         get_fdlc = input("\nDo you want to proceed with the addition?Enter your choice(Y/N): ")
         if get_fdlc.upper()=="Y":
             file_list.extend(file_list_temp) 
             print(Fore.GREEN+"Done! Added to the List!")  
         elif get_fdlc.upper()!="Y":
             print(Fore.GREEN+"Okay! Skipped those files!")     

#Remove Duplicates and Print Files 
parse_filecrypt()
file_list = list(set(list(map(os.path.realpath, file_list))))
print(f"\n{'Files' if len(file_list)>1 else 'File'} to be opened:\t\t")
for ind,fl in enumerate(file_list):
    print(Fore.GREEN+f"\t\t{ind+1}. {os.path.basename(fl)}")

#Run Through each File
for fl in file_list:
      flcount+=1
      if not os.path.isfile(fl):
          #If the File is not found!
          if(flcount==len(file_list)):
              print(Fore.RED+f'\nERROR: File path "{fl}" does not exist.')
              display_summary()
              sys.exit()
          else:
              print(Fore.RED+f'\nERROR: File path "{fl}" does not exist!')
              print("Moving to next file...")
              print("\n######################################################################################################")
              continue 
      elif os.path.splitext(os.path.basename(fl))[1] not in ('.txt','.dlc'):
          #If Unsupported File is entered!
          if(flcount==len(file_list)):
              print(Fore.RED+f'\nERROR: Inavlid File: "{os.path.basename(fl)}"\n"{os.path.splitext(os.path.basename(fl))[1]}" format is not supported!\n'+Fore.RESET+'You can only add ".dlc" or ".txt" files or any web Links.')
              display_summary()
              sys.exit()
          else:
              print(Fore.RED+f'\nERROR: Inavlid File: "{os.path.basename(fl)}"\n"{os.path.splitext(os.path.basename(fl))[1]}" format is not supported!\n'+Fore.RESET+'You can only add ".dlc" or ".txt" files or any web Links.')
              print("Moving to next file...")
              print("\n######################################################################################################")
              continue 
      else:
          flcount_parsed+=1
          file_skipped= True
          zipp_link = False
          pixel_link = False
          url_list=[]
          print(f'\nOpening File {flcount} of {len(file_list)}: "{os.path.basename(fl)}"\nLocated at: "{os.path.realpath(fl)}"\n')    
          if os.path.splitext(os.path.basename(fl))[1] == '.txt':
              print("Reading from text file...")
              file1 = open(fl, 'r')
          elif os.path.splitext(os.path.basename(fl))[1] == '.dlc':
              print("Reading from dlc file...")
              url_list += read_dlc(path=fl)
              temp_file=f"temp_{datetime.now().strftime('%d_%m__%H_%M_%S')}.txt"
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
                  total_lines_parsed+=lines_parsed
                  if fl.lower().endswith('.dlc'):
                     remove(temp_file)
                  if(zipp_link):
                     file2.close()
                     print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
                  if(pixel_link):
                     file3.close()
                     print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
                  if(flcount!=len(file_list)):
                     print(f'\nFile: "{os.path.basename(fl)}" successfully parsed!\nMoving to next file...')
                     print("\n######################################################################################################")
                  if(flcount==len(file_list)):
                     display_summary()
                     sys.exit()
                  break
              elif not line.strip() or line.strip()[0:4] !="http":
                  print(Fore.YELLOW+f'No Link found on Line {lines_parsed}:"'+line.strip()+'" it is either Empty or Invalid\n\tMoving to next line....\n')
                  continue 
              else:
               try:  
                  try:
                     if(line.find('zippy')!=-1): 
                         dl_Links=f"Links/{os.path.splitext(os.path.basename(fl))[0]}_dl_links.txt"
                         dup = check_dup(dl_Links,file_skipped)
                         if dup==0:
                           break
                         file2 = open(dl_Links, "a")
                         browser.get(line)
                         file_skipped = False
                         link_count += 1 
                         link_count_tot +=1
                         print(f'Link {link_count_tot}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ') 
                         element = browser.find_element_by_xpath("//*[@id='dlbutton']")
                         if START_DOWNLOADING:
                             element.click()
                         element = element.get_attribute("href")
                         file2.write(element+"\n")
                         dlcount+=1 
                         zipp_link = True 
                     elif(line.find('pixeldrain')!=-1):
                         dl_Links=f"Links/{os.path.splitext(os.path.basename(fl))[0]}_dl_links.txt"
                         dup = check_dup(dl_Links,file_skipped)
                         if dup==0:
                           break
                         file3 = open(dl_Links, "a")
                         # browser.get(line)
                         file_skipped = False
                         link_count += 1 
                         link_count_tot += 1
                         print(f'Link {link_count_tot}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ') 
                         element = "https://pixeldrain.com/api/file/"+line.split('/')[4]+"?download"
                         file3.write(element+"\n")
                         dlcount+=1 
                         pixel_link = True 
                     elif(line.find('sharer')!=-1):                         
                         browser.get(line) 
                         link_count += 1 
                         link_count_tot += 1
                         element = browser.find_element_by_xpath("//*[@id='btndl']")
                         print(f'Link {link_count_tot}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ')
                         try:
                            browser.find_element_by_xpath("//*[@id='overlay']").click()
                         except:
                            pass   
                         element.click()
                         sleep(0.1)
                         tab_count = open_newtab(tab_count,silent=True)
                         dlcount+=1
                     elif(line.find('drive')!=-1):
                         if(line.find('uc?')!=-1):
                            modified_drive_link = line.replace("uc?","open?") 
                            browser.get(modified_drive_link)
                            link_count += 1 
                            link_count_tot += 1
                            print(f'Link {link_count_tot}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ') 
                         print(Fore.RED+"Could not find the download link\n\tProceeding to next..\n\n")
                         tab_count = open_newtab(tab_count,silent=True)
                         continue 
                     else:
                       browser.get(line)
                       link_count += 1 
                       link_count_tot += 1
                       print(f'Link {link_count_tot}: "{line.strip()}" found on Line {lines_parsed}.\n\tLink successfully opened.\n\t\tProceeding to download file.... ')
                       raise NoSuchElementException 
                  except NoSuchElementException:
                     print(Fore.RED+"Could not find the download link\n\tProceeding to next..\n\n")
                     tab_count = open_newtab(tab_count,silent=True,script="window.open('https://www.google.com','_blank');")
                     continue 
                  print(Fore.GREEN+f"\nDownload successfully started for Link {link_count_tot}: {line.strip()}\n\tProceeding to next link.....\n")
               except WebDriverException:
                   link_count_tot += 1
                   print(Fore.RED+f"Unable to open Link {link_count_tot}: {line.strip()}\n")
                   for i in range(RETRY_COUNT):
                       sleep(0.5)
                       browser.refresh()
                       print(Fore.YELLOW+f"Refreshing page...\tRetry: {i+1}",end="\r")
                       if(i==RETRY_COUNT-1):
                           print(Fore.RED+f"\n\nMoving to next Link...\tRetried count: {i+1}\n")    
                   sleep(0.5)
                   tab_count = open_newtab(tab_count,silent=True,script="window.open('https://www.google.com','_blank');")
                   continue 