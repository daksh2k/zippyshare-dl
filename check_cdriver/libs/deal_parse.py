import requests
from bs4 import BeautifulSoup

try : 
    from check_cdriver.libs import deal_reg
except Exception :
    import check_cdriver.libs.deal_reg as deal_reg


BASE_URL = "https://chromedriver.chromium.org/downloads"


def get_to_URL(url):
    req = requests.get(url)
    if req.status_code == 200 and req.ok:
        return req
    print("request error")


def parse_driver_version():
    base_req = get_to_URL(BASE_URL)
    base_soup = BeautifulSoup(base_req.content, "html.parser")

    atags = base_soup.select("a")

    return atags


def parse_download_URL(local_browser_ver_code):
    atags = parse_driver_version()

    for a in atags:
        # print(a.text)
        version = deal_reg.reg_from_atags(a.text)
        if deal_reg.is_version(version):
            version_code = deal_reg.reg_version_code(version)
            if version_code == local_browser_ver_code:
                download_url = "/".join(
                    [
                        "https://chromedriver.storage.googleapis.com",
                        version,
                        "chromedriver_win32.zip",
                    ]
                )
                return download_url, version


# def parse_driver_version(soup):
#     # print(soup)
#     li = soup.select(".sites-layout-tile.sites-tile-name-content-1 > div li")
#     href = li[0].select_one("a")["href"]
#     version = deal_reg.regrex_version(href)
#     # https://chromedriver.storage.googleapis.com/78.0.3904.105/chromedriver_win32.zip
#     return version
