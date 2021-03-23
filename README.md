# Zippyshare downloader and Links Extractor and Automator
Python script to automatically download from Zippyshare using [Selenium package](https://www.selenium.dev/) and [Internet Download Manager](https://www.internetdownloadmanager.com/).\
Download [IDM](https://www.internetdownloadmanager.com/download.html) from here for downloading multiple files.\
The links should be in a text file or a dlc file. The **file can contain links in any way,** but can contain only one link per line.\
The script can skip invalid or empty lines to move to the next line until EOF is reached and then it will auto exit.\
EOF is calculated using 2 empty lines, the script auto exits if it encounters 2 empty lines in a row.\


## To run clone this repositary and create a virtual environment and install dependencies from [requirements.txt](./requirements.txt) file.
```python
git clone https://github.com/daksh2k/zippyshare-dl.git
pip install virtualenv
py -m venv "Your name of the environment" #Add any name without inverted commas
py -m venv env
pip install -r requirements.txt
```

### Then run the [linkdl.py](./linkdl.py) file and enter the path to the text file containing the links in the console argument.
### If you just want Download Links then run [testaltdl.py](./testaltdl.py), it will save all the links in a txt file in the current directory.(Also supports multiple files)
#### Then you can add that file to any downloader.

For example :
```python
py linkdl.py abc.txt  #if in the same folder otherwise add full path
py linkdl.py #if no argument is passed, the program will ask for the path
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

