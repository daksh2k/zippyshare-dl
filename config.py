import os

#CONFIG VARS
ADD_EXTENSIONS     =  1      # Add Adblocker and IDM Extension to the Browser Instance
DEBUG_ADDRESS      =  0      # Connect to already Running Browser on a debug port
START_DOWNLOADING  =  0      # Start Downloading from Links Directly or just save in a text file.
DIR_CHECK          =  1      # If you Want to Auto Add files dlc and txt files from certain directories
SKIP_DUP           =  0      # Skip Duplicate Check For Files 
MULTILINE_INPUT    =  1      # Accept Multiline Input or Not
CDRIVER_CHECK      =  1      # Whether to Auto Update Chrome Driver According to the version of Chrome Browser
SKIP_DEAD          =  3      # Skip file after certain number of Links are found Dead.Put 0 for not skipping.
RETRY_COUNT        =  2      # Retry If unable to Open Link Min value=1 
DIRS_TO_CHECK      =  ('.','./Links',os.path.expanduser("~")+"\\Downloads")                   # Following Dirs to automatically check for dlc and text files.
COMMON_NAMES       =  ("req.*\.txt",".*dl_links\.txt","temp_.*",".*\d{2}_\d{2}_\d{4}\.txt")   # Common Names to Ignore from Directory, Supports Regex