#!/usr/bin/env python3

from pathlib import Path
import requests
from datetime import timedelta, datetime

# This script is a cron job which reads the list of sites being
# tracked and updates the appropriate log files to record how
# long each site took to respond to its request.

def main():
    sites = read_sites()

    for site in sites:
        check_site(site)


def check_site(site):
    url = "https://"+site

    log_file = site.replace("/","_")
    
    log_path = Path(__file__).parent.parent / "data" / log_file

    try:
        response = requests.get(url=url, timeout=30)
        status = response.status_code
        elapsed = response.elapsed / timedelta(milliseconds=1)

    except requests.exceptions.RequestException:
        status = "FAIL"
        elapsed=30000


    with open(log_path, "at", encoding="utf8") as out:
        date,time = str(datetime.now()).split()
        time= time.split(".")[0]
        line = [date,time,str(status),str(elapsed)]
        print("\t".join(line), file=out)


def read_sites():

    site_list = Path(__file__).parent / "site_list.txt"

    sites = []

    with open(site_list,"rt",encoding="utf8") as infh:
        for line in infh:
            sites.append(line.strip())

    return sites



if __name__ == "__main__":
    main()

