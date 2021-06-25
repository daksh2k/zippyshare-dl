import os
import re
import zipfile
import platform
import datetime
from bs4 import BeautifulSoup
import requests

try:
    from check_cdriver.libs import deal_parse, deal_reg, deal_zip, deal_txt
except Exception:
    import check_cdriver.libs.deal_parse as deal_parse
    import check_cdriver.libs.deal_reg as deal_reg
    import check_cdriver.libs.deal_zip as deal_zip
    import check_cdriver.libs.deal_txt as deal_txt

def is_file_exists(driver_path):
    try:
        if not os.path.isfile(driver_path):
            print(f"{driver_path} does not exist!")
            driver_exists = False
            return driver_exists
        driver_exists = True
        return driver_exists     
    except Exception as e:
            print(e)

def compare_driver(driver_exists):
    try:
        driver_ver = deal_txt.read_version(driver_mother_path)
        driver_ver_code = deal_reg.reg_version_code(driver_ver)
        print("chromedriver_ver : {}".format(driver_ver))
        if driver_ver_code == browser_ver_code and driver_exists:
            return True
    except FileNotFoundError:
        pass

def check_browser_ver():
    check_files_dirs = ["C:/Program Files (x86)","C:/Program Files"]
    try:
        if platform.architecture()[0] != "64bit":
            ver_path = "C:/Program Files/Google/Chrome/Application"
        else:
            for dirs in check_files_dirs:
                dir_p = dirs
                if 'Google' in os.listdir(dirs):
                    if 'Chrome' in os.listdir(dir_p+"/Google"):
                        ver_path = dir_p+"/Google/Chrome/Application"
        for i in os.listdir(ver_path):
            if deal_reg.is_version(i):
                return i
    except Exception:
        print("You do not have Chrome browser.")

def make_dir():
    try:
        os.makedirs(driver_mother_path)
    except OSError as e:
        if e.errno != 17:
            raise

def main():
    driver_path = os.path.join(os.path.realpath(driver_mother_path), "chromedriver.exe")
    driver_exists = is_file_exists(driver_path)
    if compare_driver(driver_exists):
        return
    make_dir()
    temp = deal_parse.parse_download_URL(browser_ver_code)
    down_url,new_version = temp
    download_path = os.path.join(driver_mother_path, "chromedriver.zip")
    print("Chromedriver does not match your Chrome browser version. Downloading...")
    r = requests.get(down_url)
    open(download_path, 'wb').write(r.content)
    print("Download Complete!")
    deal_zip.unzip(driver_mother_path, download_path)
    deal_zip.remove_zip(download_path)
    deal_txt.write_version(driver_mother_path, new_version)

driver_mother_path = "./chromedriver/"
browser_ver = check_browser_ver()
print("chromebrowser_ver : {}".format(browser_ver))
browser_ver_code = deal_reg.reg_version_code(browser_ver)

if __name__ == "__main__":
    main()