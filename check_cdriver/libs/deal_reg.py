import re


def reg_from_atags(atag):
    try:
        m = re.compile("ChromeDriver (.*)")
        p = m.search(atag)
        version = p.group(1)
        return version
    except AttributeError:
        pass


def regrex_version(href):
    p = re.compile(".*path=(.*)/")
    m = p.search(href)
    return m.group(1)


def reg_version_code(ver):
    try:
        m = re.compile("(\d*)\..*")
        p = m.search(ver)
        return p.group(1)
    except AttributeError:
        pass


def is_version(text):
    try:
        m = re.compile("(\d*)\..*")
        p = m.search(text)
        int(p.group(1))
        return True
    except Exception:
        pass
