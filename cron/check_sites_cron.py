#!/usr/bin/env python3

from pathlib import Path
import requests
from datetime import timedelta, datetime
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# This script is a cron job which reads the list of sites being
# tracked and updates the appropriate log files to record how
# long each site took to respond to its request.

def main():
    sites = read_sites()

    for site in sites:
        check_site(site)


def check_site(site):
    url = "https://"+site[0]

    log_file = site[0].replace("/","_")
    
    log_path = Path(__file__).parent.parent / "data" / log_file

    try:
        response = requests.get(url=url, timeout=30)
        status = response.status_code
        elapsed = response.elapsed / timedelta(milliseconds=1)

        if status != 200:
            send_email(site,str(status))

    except requests.exceptions.RequestException:
        status = "FAIL"
        elapsed=30000
        send_email(site,status)


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
            sites.append((line.strip().split()[0],line.strip().split()[1:]))

    return sites


def send_email(site,status):
    
    # Check if we're alerting for this site
    if not site[1]:
        return


    # Check if we've already sent an alert recently
    flag_file = site[0].replace("/","_")    
    flag_path = Path(__file__).parent.parent / "alert_flags" / flag_file

    if flag_path.exists():
        # Check if the modified time is in the last hour
        modified_time = datetime.fromtimestamp(flag_path.stat().st_mtime)
    
        if datetime.now() - modified_time < timedelta(hours=1):
            # We sent something within the last hour
            return

    # If we get here then we're sending an email so we need to create or
    # update the flag file
    with open(flag_path,"w"):
        pass

    message = f"The {site[0]} site has stopped responding correctly\n\nThe last request generated a status of {status}\n\nSomeone should take a look\n\nThis message was sent automatically by the ResponseMonitor system"

    port = 25

    msg = MIMEMultipart()
    msg['From'] = 'babraham.bioinformatics@babraham.ac.uk'
    msg['To'] = ", ".join(site[1])
    msg['Subject'] = "[ResponseMonitor] "+site[0]+" is unresponsive"
    message = message
    msg.attach(MIMEText(message))


    smtp = SMTP()
    smtp.connect("localhost",port)

    smtp.sendmail(from_addr="contact@biotrain.tv",to_addrs=site[1], msg=msg.as_string())


if __name__ == "__main__":
    main()

