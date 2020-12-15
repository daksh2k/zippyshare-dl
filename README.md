# Zippyshare downloader and Links opener
Python script to automatically download from Zippyshare using [Selenium package](https://www.selenium.dev/) and [Internet Download Manager](https://www.internetdownloadmanager.com/).\
Download [IDM](https://www.internetdownloadmanager.com/download.html) from here for downloading multiple files hassle free.\
The links should be in a text file. The ** file can contain links in any way, ** but can contain only one link per line.\
The script can skip invalid or empty lines to move to the next line until EOF is reached.\ 
If not a Zippyshare link then all the links will be opened in new tabs to download the file manually.


### To run create a virtual environment and install dependencies from [requirements.txt](./requirements.txt).
```
pip install venv
py -m venv "Your name of the environment"
py -m venv env
pip install requirements.txt
```

This also installs 2 extensions adblock and idm to work without any hassle.

### Then run the [linkdl.py](./linkdl.py) file and enter the path to the txt file containing the links in the console argument.
For example :
```python
py linkdl.py abc.txt  #if in the same folder otherwise add full path
py linkdl.py #if no argument is passed, the program will ask for the path before opening the browser
```

It uses selenium package to open links in a browser and find the download button using xpath on Zippyshare.\
It also works on other sites just change the location in the line where download button is situated.\
You can find any element by id,tag,class,path etc.\
For more info visit official [Selenium documentation](https://selenium-python.readthedocs.io/locating-elements.html)

```python
element = browser.find_element_by_xpath("//*[@id='dlbutton']")
element.click()
```
If it does not find the download link then NoSuchElementException will be thrown it will open all the links in the browser in new tabs(Works on any site)


Using this
```python
browser.execute_script("window.open('');")
browser.switch_to.window(browser.window_handles[count+2])
```


