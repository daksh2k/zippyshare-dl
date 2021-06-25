# Zippyshare downloader and Links Extractor
Python script to automatically download from Zippyshare using [Selenium package](https://www.selenium.dev/) and [Internet Download Manager](https://www.internetdownloadmanager.com/).\
Download [IDM](https://www.internetdownloadmanager.com/download.html) from here for downloading multiple files.

1. ### The Links will be saved in a text file which can then be imported to idm from: 
   Tasks>Import>from text file

2. Other option is set the `START_DOWNLOADING` variable to True in the [main.py](./main.py) file   
 which will start downloading instantly. (Useful for less Links) 
3. See [here](https://github.com/daksh2k/zippyshare-dl/blob/e3acb52c513ea6918e5fbb436c245879b453e89f/main.py#L14-L22) for more configurable options. 

## Requirements/Installation
- Platform - Windows only.
- Chrome Browser.
- Chromedriver(Included). 
- Python >= v3.6
- Install requirements yourself by running the following commands from powershell:
  ``` bash
  git clone https://github.com/daksh2k/zippyshare-dl.git
  cd zippyshare-dl
  pip install virtualenv
  python -m venv env
  env/scripts/activate.ps1
  pip install -r requirements.txt
  ```

- Or simply Install via the [install.ps1](./install.ps1) script after cloning/downloading the repositary.

 
## Features
- Supported formats:
  - `.txt`
  - `.dlc`
  - Filecrypt Links
  - Pass any web link directly in arguments or input or through a file.
- Parse from Multiple Files. 

  Example-:
  
   `python main.py test.dlc https://filecrypt.co/Container/31B1864087.html test2.txt Links/test3.txt`
- Directly parse from filecrypt links.(Only those links without recaptcha)
- Automatically get recently created(within last 24 hours)  `.dlc` and `.txt` files from certain folders.
   ![alt text](./examples/autopick.png "Autopick")
- Duplicate check to see if file is already parsed.
- Automatically Update chromedriver if out of date.
- Support for Sharer.pw Links, for  directly clicking Download button.
- Skips Empty or Invalid Lines in the File.
     ![alt text](./examples/invalid.png "Invalid")
- Summary after completion.
     ![alt text](./examples/summary.png "Summary")
- Open all Links in new tab in the browser if unsupported Links.
- Retry Links if unable to Load.  
  ![alt text](./examples/unable.png "Unable")


It uses Selenium package to open links in a browser and find the download button using xpath on Zippyshare.\
You can find any element by id,tag,class,path etc.\
For more info visit official [Selenium documentation](https://selenium-python.readthedocs.io/locating-elements.html).

```python
element = browser.find_element_by_xpath("//*[@id='dlbutton']")
```



