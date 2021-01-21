# cd D:/College/Projects/zippyshare-dl/Links
D:/College/Projects/zippyshare-dl/env/Scripts/activate
chrome.exe -remote-debugging-port=4000 --user-data-dir="D:/College/Projects/zippyshare-dl/Selenium/Chrome_Test_Profile"
start "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
py D:/College/Projects/zippyshare-dl/linkdl.py | tee -a D:/College/Projects/zippyshare-dl/Logs/log_linkdl.txt
deactivate
