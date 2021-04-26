# Zippyshare downloader and Links Extractor and Automator
Python script to automatically download from Zippyshare using [Selenium package](https://www.selenium.dev/) and [Internet Download Manager](https://www.internetdownloadmanager.com/).\
Download [IDM](https://www.internetdownloadmanager.com/download.html) from here for downloading multiple files.\
The links should be in a text file or a dlc file. The **file can contain links in any way,** but can contain only one link per line.

1. ### **The Links will be saved in a text file which can then be imported to idm from:** 
   <span style="color: red">
   Tasks>Import>from text file
   </span>
2. Other option is the second [Script](./linkdl.py) which will start downloading instantly. (Useful for less Links) 

## Installation

Ensure you have Python Installed.
python >= v3.2

Download for your individual platforms [here](https://www.python.org/downloads)

You can use either of these options to use the script:
- Install yourself by running the following commands from powershell:

  ``` bash
  git clone https://github.com/daksh2k/zippyshare-dl.git
  cd zippyshare-dl
  pip install virtualenv
  python -m venv "Your name of the environment" #Add any name without inverted commas
  python -m venv env
  env/scripts/activate
  pip install -r requirements.txt
  ```

- Or simply Install via the [install.ps1](./install.ps1) after cloning/downloading the repositary:

  ``` bash
  git clone https://github.com/daksh2k/zippyshare-dl.git
  ```
## Usage
-  For saving dl Links to text file. You can run manually from powershell (Can pass multiple files in args)
 ``` bash
  env/scripts/activate
  python main.py abc.txt  #if in the same folder otherwise add full path
  python main.py #if no argument is passed, the program will ask for the path
  ```
- Or simply run via the [run.ps1](./run.ps1) after installing:
- If you directly want to start downloading then run this script [linkdl.py](./linkdl.py) (Only single file)
  ``` bash
  env/scripts/activate
  python linkdl.py abc.txt  #if in the same folder otherwise add full path
  python linkdl.py #if no argument is passed, the program will ask for the path
  ```

It uses Selenium package to open links in a browser and find the download button using xpath on Zippyshare.\
It also works on other sites just change the location in the line where download button is situated.\
You can find any element by id,tag,class,path etc.\
For more info visit official [Selenium documentation](https://selenium-python.readthedocs.io/locating-elements.html)

```python
element = browser.find_element_by_xpath("//*[@id='dlbutton']")
element.click()
```
If it does not find the download link then NoSuchElementException will be thrown it will open all the links in the browser in new chrome tabs(**Works on any site**)

