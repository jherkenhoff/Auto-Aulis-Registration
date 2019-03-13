import logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
import time
import os
import sys
import datetime
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By as by

# SETTINGS:
######################################################
credentials_path       = "~/aulis-credentials.txt"
aulis_base_url         = "https://www.aulis.hs-bremen.de/"
aulis_group_url        = "https://www.aulis.hs-bremen.de/ilias.php?ref_id=1007806&cmdClass=ilrepositorygui&cmdNode=t6&baseClass=ilrepositorygui"
desired_group_selector = "#lg_div_1007810_pref_1007806 h4 > a"
######################################################

# Read credentials from file
credentials_file = open(os.path.expanduser(credentials_path))
username = credentials_file.readline().rstrip()
password = credentials_file.readline().rstrip()

# Open Aulis
browser = webdriver.Firefox()
browser.get(aulis_base_url)
browser.find_element_by_id("username").send_keys(username)
browser.find_element_by_id("password").send_keys(password)
browser.find_element_by_css_selector("input.btn").click()
browser.get(aulis_group_url)


def plot_intervals(timestamps, access_interval):
    plt.plot(timestamps, access_interval)
    plt.ylabel("Interval / s")
    plt.xticks(rotation='vertical')
    plt.savefig("access-interval.png")


# Wait until the registration is open
attempt = 0
access_interval = []
timestamps = []
while(True):
    attempt += 1
    try:
        # Reload page
        tic = time.perf_counter()
        browser.get(aulis_group_url)
        toc = time.perf_counter()
        access_interval.append(toc-tic)
        timestamps.append(datetime.datetime.now())
        # Try to click on group link
        elem = browser.find_element_by_css_selector(desired_group_selector)
        elem.click()
        logging.info("REGISTRATION OPEN (on attempt %d)" % attempt)
        break
    except KeyboardInterrupt:
        plot_intervals(timestamps, access_interval)
        sys.exit()
    except:
        os.system("beep -f 400 -l 10")
        logging.info("Closed (Attempt %d interval: %.2f)" % (attempt, (toc-tic)))

# Accept registration:
try:
    browser.find_element_by_name("cmd[join]").click()
    os.system("beep -f 900 -l 100")
    logging.info("REGISTRATION COMPLETED !!!!!")
except:
    logging.error("Exception during registration !!!!!")
    os.system("beep -f 400 -l 600")

# Check registration
try:
    browser.find_element_by_class_name("alert-success")
    logging.info("Assert success: Message visible")
    os.system("beep -f 700 -l 100")
except:
    logging.warning("Something went wrong? (Message not visible)")
    os.system("beep -f 500 -l 100")

try:
    browser.find_element_by_id("tab_grp_btn_unsubscribe")
    logging.info("Assert success: Unsubscribe button visible")
    os.system("beep -f 800 -l 100")
except:
    logging.warning("Something went wrong? (Unsubscribe button not present)")
    os.system("beep -f 500 -l 100")

os.system("beep -f 900 -l 100")

plot_intervals(timestamps, access_interval)
browser.save_screenshot('screenshot.png')
