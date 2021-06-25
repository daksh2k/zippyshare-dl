import os

import zipfile


def unzip(driver_mother_path, download_path):
    try:
        with zipfile.ZipFile(download_path) as zf:
            zf.extractall(path=driver_mother_path)
    except Exception as e:
        print(e)


def remove_zip(download_path):
    os.remove(download_path)