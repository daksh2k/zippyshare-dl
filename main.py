import os
import sys
import re
import requests

from time import sleep,time
from datetime import datetime

# For parsing DLC files
from dcryptit import read_dlc

#Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException,WebDriverException,ElementNotInteractableException

# For colored output to Terminal
from colorama import Fore,init
init(autoreset=True)

#Get The Config Variables
import config as c

# SUMMARY VARS 
link_count         = 0
link_count_tot     = 0
tab_count          = 0
lines_parsed       = 0
dlcount            = 0
flcount            = 0
flcount_parsed     = 0
total_lines_parsed = 0
FILECRYPT_DOMAIN   = "https://www.filecrypt.cc/"
file_list          = []
file_list_temp     = []
start_time         = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
exec_start_time    = time()
to_sub             = 0

#Get dlc from Filecrypt Links
def parse_filecrypt(tab_count):
   unsuc  = set()
   to_remove = set()
   for index,item in enumerate(file_list):
      if(item.find('filecrypt')!=-1):
           print(f"\nFound filecrypt Link: {item}")
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
                          os.remove(file_path)
                      else:
                          file_list[index] = file_path
                          print(Fore.YELLOW+f"{file_path} already exists\n\tSkipping Download...")
                          continue
                   r = requests.get(link_to_download)
                   open(file_path, 'wb').write(r.content)
                   file_list[index] = file_path
               except Exception as e: 
               	   print(Fore.RED+f"\n❌ Unable to find DLC \n{item} is not supported. Try opening the link manually.")
                   unsuc.add(item)
                   tab_count = open_newtab(tab_count)
                   continue
           except Exception as e:
                print(Fore.RED+f"[*] {e}")
                unsuc.add(item)
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
           to_remove.add(patt) 
   return tab_count,unsuc,to_remove

#Open new Tab in the browser
def open_newtab(tab_count,silent=True,script="window.open('');"):
   if not silent:
      print("Moving to next.....")
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
           print(Fore.YELLOW+"File exists but with size 0\nDeleteing File and Downloading Again")
           os.remove(dl_Links)
       else:
          global to_sub
          in_time = time()
          skip = input(f"Dl_Links File {dl_Links} already exists.\nDo you want to skip downloading?(Y/N):  ")
          in_time = time() - in_time
          to_sub += in_time 
          if(skip.upper()=="Y"):
               file_skipped = True
               print(Fore.GREEN+f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
               file1.close()	
               if flcount!=len(file_list):
                    print("Moving to next.....")
                    print("\n######################################################################################################")
                    return 0   
               display_summary()
               sys.exit()
          else:
               file_skipped = False
               print("\nDownloading Links again.....\n") 
               os.remove(dl_Links)

#Print the relevant statistics after completion.       
def display_summary():
   time_taken = time() - exec_start_time - to_sub
   print("\n############################  Summary   ##################################################")
   print(f"\nLinks successfully opened: {link_count}/{link_count_tot}\nTotal downloads started: {dlcount}\nTotal files parsed for Links: {flcount_parsed}/{flcount}\nTotal Lines Parsed: {total_lines_parsed}")
   print(f"Time taken: {time_taken:.2f} seconds\n\nExiting.....\n\n")
   print(f"Process ended on Date and Time: {datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')}\n\n")
   for item in to_remove:
           os.remove(item)
   if len(browser.window_handles)==1:
            browser.close()

cwd = os.getcwd()
os.system("cls")
print(f"Process started on Date and Time: {start_time}")
print(f"Current working directory: {cwd}\n")

# Check if Chrome Driver is Updated or not 
if c.CDRIVER_CHECK:
    import check_cdriver.Check_Chromedriver as cd_check 
    cd_check.driver_mother_path = "./Selenium"
    cd_check.main()

options = webdriver.ChromeOptions()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--allow-insecure-localhost')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('user-data-dir='+cwd+'\\Selenium\\Chrome_Test_Profile') 
if c.ADD_EXTENSIONS:
    options.add_extension('./Selenium/Extensions/ublock.crx')
    options.add_extension('./Selenium/Extensions/idm.crx')
if c.DEBUG_ADDRESS:
    options.add_experimental_option("debuggerAddress", "localhost:4000")
caps = DesiredCapabilities.CHROME
caps['acceptInsecureCerts']= True
print("\nOpening browser\nThis process will take a few seconds.....")

#Connecting with WebDriver
try:
    browser = webdriver.Chrome('./Selenium/chromedriver',options=options,desired_capabilities=caps)
except Exception as e:
    print(Fore.RED+f"[*] {e}")
    browser = webdriver.Chrome('./Selenium/chromedriver',desired_capabilities=caps)
print(Fore.GREEN+"✅ Browser opened.....")
browser_len = len(browser.window_handles) #fetching the Number of Opened tabs
if browser_len > 1: 
      browser.switch_to.window(browser.window_handles[0]) # Switching the browser focus to First tab.

#Creating Folder links to store the files
if not os.path.exists('Links'):
      print("Creating Folder Links to store download Links.....\n")
      os.makedirs('Links')

#Parse Input fron Arguments or By taking Input
if len(sys.argv)<2:
      if c.MULTILINE_INPUT:
          print("\nEnter the names of the Files or paste Links directly.Enter Ctrl-Z to save it: ")
          while True:
              try:
                input_line = input()
              except EOFError:
                break  
              if input_line.strip().strip('"')!="":
                  file_list.append(input_line.strip().strip('"'))
      else:
          file_list = [fl.strip().strip('"') for fl in input("\nEnter the name of the file or path(if multiple separete by commas): ").strip().split(',') if fl.strip().strip('"')!=""]  
else: 
      file_list = [sys.argv[i] for i in range(1,len(sys.argv))]

#Remove Duplicates 
tab_count,unsuc,to_remove = parse_filecrypt(tab_count)
file_list = list(set(map(os.path.realpath, set(file_list)-unsuc)))

#Automatically Add Files from Certain Directories
if c.DIR_CHECK:
     c.DIRS_TO_CHECK = list(set(map(os.path.realpath,c.DIRS_TO_CHECK)))
     val = re.compile('|'.join(c.COMMON_NAMES))
     for dirParse in c.DIRS_TO_CHECK:
         for entry in os.scandir(dirParse):
             full_p = os.path.join(dirParse, entry.name)
             if entry.is_file() and re.match(val,entry.name) is None and full_p not in file_list and os.path.splitext(entry.name)[1].lower() in (".txt", ".dlc") and (exec_start_time - os.path.getctime(full_p))/3600 < 24:
                    file_list_temp.append(full_p)   
     if len(file_list_temp)>0:
         print("\nGetting \".dlc\" and \".txt\" files from: \n\t\t"+Fore.YELLOW+'\n\t\t'.join(c.DIRS_TO_CHECK)+Fore.RESET+"\n")
         print("Following files(Created within last 24 hours) can be added to the File list: \t")
         for ele in file_list_temp:
              print(Fore.CYAN+f"\t\t{os.path.basename(ele)}")           
         get_fdlc = input("\nDo you want to proceed with the addition?Enter your choice(Y/N): ")
         if get_fdlc.upper()=="Y":
             file_list.extend(file_list_temp) 
             print(Fore.GREEN+"✅ Added to the List!")  
         elif get_fdlc.upper()!="Y":
             print(Fore.GREEN+"❌ Skipped those files!")     
if not file_list:
    print(Fore.RED+"ERROR: No Files Added!\nExiting.....")
    browser.close()
    sys.exit()
print(f"\n{'Files' if len(file_list)>1 else 'File'} to be opened:\t\t")
for ind,fl in enumerate(file_list):
    print(Fore.GREEN+f"\t\t{ind+1}. {os.path.basename(fl)}")

exec_start_time = time()

#Run Through each File
for fl in file_list:
      flcount+=1
      link_count_z=0
      dlcount_z=0
      if not os.path.isfile(fl):
          #If the File is not found!
          print(Fore.RED+f'\nERROR: File path "{fl}" does not exist!')
          if(flcount==len(file_list)):
              display_summary()
              sys.exit()
          print("\n######################################################################################################")
          continue 
      elif os.path.splitext(os.path.basename(fl))[1] not in ('.txt','.dlc'):
          #If Unsupported File is entered!
          print(Fore.RED+f'\nERROR: Inavlid File: "{os.path.basename(fl)}"\n"{os.path.splitext(os.path.basename(fl))[1]}" format is not supported!\n'+Fore.RESET+'You can only add ".dlc" or ".txt" files or any web Links.')
          if(flcount==len(file_list)):
              display_summary()
              sys.exit()
          print("\n######################################################################################################")
          continue 
      else:
          lines_parsed=0
          flcount_parsed+=1
          file_skipped = True
          zipp_link = False
          pixel_link = False
          url_list=[]
          print(f'\nFile {flcount} of {len(file_list)}: "{os.path.basename(fl)}"\nLocated at: "{fl}"\n\n')    
          if os.path.splitext(os.path.basename(fl))[1] == '.txt':
              file1 = open(fl, 'r')
          elif os.path.splitext(os.path.basename(fl))[1] == '.dlc':
              url_list += read_dlc(path=fl)
              temp_file=f"temp_{datetime.now().strftime('%d_%m__%H_%M_%S')}.txt"
              file1 = open(temp_file, "w")
              for url in list(url_list): 
                  file1.write(url+"\n")
              file1.close()
              file1 = open(temp_file, 'r')
              to_remove.add(temp_file)  
          line= file1.readline()
          x=[line]
          while True:
              lines_parsed+=1
              line2= file1.readline()
              x.append(line2)
              line=x[lines_parsed-1]
              if not line.strip() and not line2.strip():
                  file1.close()
                  total_lines_parsed+=lines_parsed
                  if zipp_link or pixel_link:
                     print(f'\n\nDownload Links saved to file "{os.path.basename(dl_Links)}"\nLocated at "{os.path.realpath(dl_Links)}"')
                     try: 
                       file2.close()
                       file3.close()
                     except NameError:
                       pass  
                  print(Fore.GREEN+f'\nFile: "{os.path.basename(fl)}" successfully parsed!')
                  if(flcount==len(file_list)):
                     display_summary()
                     sys.exit()
                  print("Moving to next.....")
                  print("\n######################################################################################################")
                  break
              elif not line.strip() or line.strip()[0:4] !="http":
                  print(Fore.YELLOW+f'No Link found on Line {lines_parsed}:"'+line.strip()+'" it is either Empty or Invalid\n')
                  continue 
              else:
               try:  
                  try:
                     if line.count('zippyshare')==0 and line.count('pixeldrain')==0:
                        link_count_tot += 1
                        print(f'Link {link_count_tot}: "{line.strip()}" on Line {lines_parsed}.')
                     if(line.find('zippyshare')!=-1): 
                         dl_Links=f"Links/{os.path.splitext(os.path.basename(fl))[0]}_dl_links.txt"
                         if not c.SKIP_DUP:
                             dup = check_dup(dl_Links,file_skipped)
                             if dup==0:
                                break
                         elif file_skipped:
                             try:
                                os.remove(dl_Links)
                             except (FileNotFoundError,PermissionError):
                                pass   
                         if c.SKIP_DEAD:
                             if link_count_z-dlcount_z>=c.SKIP_DEAD:
                                try:
                                    total_lines_parsed+=lines_parsed
                                    file1.close()
                                    file2.close()
                                    os.remove(dl_Links)
                                except Exception as e:
                                    print(Fore.RED+f"[*] {e}")
                                print(Fore.RED+"\nAll Links seem to be down!")
                                print(f"Skipping File: \"{os.path.basename(fl)}\"") 
                                if flcount==len(file_list): 
                                    display_summary()
                                    sys.exit()
                                print("\nMoving to next.....")  
                                print("\n######################################################################################################")
                                break
                         file2 = open(dl_Links, "a")
                         link_count_tot += 1
                         print(f'Link {link_count_tot}: "{line.strip()}" on Line {lines_parsed}.')
                         browser.get(line)
                         file_skipped = False
                         link_count += 1 
                         link_count_z +=1
                         print("✅ Opened")   
                         element = browser.find_element_by_xpath("//*[@id='dlbutton']")
                         if c.START_DOWNLOADING:
                             element.click()
                         element = element.get_attribute("href")
                         file2.write(element+"\n")
                         dlcount+=1 
                         dlcount_z+=1
                         zipp_link = True 
                     elif(line.find('pixeldrain')!=-1):
                         dl_Links=f"Links/{os.path.splitext(os.path.basename(fl))[0]}_dl_links.txt"
                         if not c.SKIP_DUP:
                             dup = check_dup(dl_Links,file_skipped)
                             if dup==0:
                                break
                         elif file_skipped:
                             try:
                                os.remove(dl_Links)
                             except (FileNotFoundError,PermissionError):
                                pass
                         file3 = open(dl_Links, "a")
                         # browser.get(line)
                         file_skipped = False
                         link_count += 1
                         link_count_tot += 1
                         print(f'Link {link_count_tot}: "{line.strip()}" on Line {lines_parsed}.')
                         print("✅ Opened") 
                         element = "https://pixeldrain.com/api/file/"+line.split('/')[4]+"?download"
                         file3.write(element+"\n")
                         dlcount+=1 
                         pixel_link = True 
                     elif(line.find('sharer')!=-1):                         
                         browser.get(line)
                         link_count += 1
                         print("✅ Opened")  
                         element = browser.find_element_by_xpath("//*[@id='btndl']")
                         try:
                            browser.find_element_by_xpath("//*[@id='overlay']").click()
                         except (ElementNotInteractableException,NoSuchElementException):
                            pass
                         element.click()
                         sleep(0.1)
                         tab_count = open_newtab(tab_count)
                         dlcount+=1
                     elif(line.find('drive')!=-1):
                         if(line.find('uc?')!=-1):
                            modified_drive_link = line.replace("uc?","open?")
                            browser.get(modified_drive_link)
                         else:
                            browser.get(line)                             
                         link_count += 1
                         print("✅ Opened")
                         print(Fore.RED+"❌ Downloaded\n")
                         tab_count = open_newtab(tab_count)
                         continue
                     else:
                       browser.get(line)
                       link_count += 1 
                       print("✅ Opened")  
                       raise NoSuchElementException 
                  except NoSuchElementException:
                     print(Fore.RED+"❌ Downloaded\n")
                     tab_count = open_newtab(tab_count)
                     continue 
                  print("✅ Downloaded\n")
               except WebDriverException:
                   print(Fore.RED+f"❌ Opened\n❌ Downloaded\n")
                   for i in range(c.RETRY_COUNT):
                       sleep(0.5)
                       browser.refresh()
                       print(Fore.YELLOW+f"Refreshing page.....\tRetry: {i+1}",end="\r")   
                   print(Fore.RED+f"\n\nMoving to next.....\tRetried count: {i+1}\n")
                   tab_count = open_newtab(tab_count,script="window.open('https://www.google.com','_blank');")
                   continue 