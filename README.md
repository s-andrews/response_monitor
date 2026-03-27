# Response Monitor

A system to monitor and review the response times of multiple websites.

![Screenshot](https://raw.githubusercontent.com/s-andrews/response_monitor/refs/heads/main/response_monitor_screenshot.png)


Response Monitor is a system into which you can enter an arbitrary number of website URLs which it will then monitor for their response times to a simple GET request.

The system has two parts:

1. A cron script which runs every 5 minutes and checks the response from each site

2. A shiny web application which allows you to view the logs and see the results in a flexible way


## Installation

To install the system simply clone this git repository to a machine you want to run the system. Ideally you will use the same machine to serve the shiny app as you use to run the tests, but you don't have to do this this way.

### Dependencies

The system expects the following dependencies to be present.

1. A recent version of python - nothing outside of the standard library is used

2. A recent version of R, into which the following packages are installed.
  * tidyverse
  * shiny
  * bslib
  * plotly
  
### System Configuration

To set up the sites to monitor you need to edit the ```cron/site_list.txt``` file.  
Put one URL (without the https:// prefix) per line into this file for all sites you want to monitor.

If you would like to have people alerted if a site becomes unresponsive then you can add as many emails as you want
after the url.  Any site not responding within 30 seconds, or which returned an HTTP status code other than 200 will
trigger an email warning to those addresses.

The email is send to a mail server running on localhost so you will need to have that configured.  If there is an extended
outage on a site it will send one email per hour until the site returns.


### Cron setup

We recommend that you monitor every 5 minutes, but you can set the interval to be whatever you prefer.  To do this you need to set up a cron job on your system.  To do that you should run

```
crontab -e
```

..then in the editor which opens enter a cron job which looks like:

```
*/5     *       *       *       *       /srv/response_monitor/cron/check_sites_cron.py
```

..but changing the path of the cron script to match where it is installed on your system.

### Shiny config

The shiny app is in the ```shiny/ResponseMonitor``` subdirectory.  Probably the easiest way to install the app is just to symlink it into the folder configured to serve Shiny apps on your system.


