def write_version(driver_mother_path, latest_version):
    with open(driver_mother_path + "/version.txt", "wt") as f:
        f.write(latest_version)


def read_version(driver_mother_path):
    with open(driver_mother_path + "/version.txt", "rt") as f:
        result = f.read()
    return result