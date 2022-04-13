"""This file contains class to perofrm webscraping"""

# Imports
import time
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
from io import StringIO
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import numpy as np
import pandas as pd



class Webscraping():
    """Performs web scraping"""

    def __init__(self, port='4444', teardown=True):
        """Instanciates the driver and defines browser options"""

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.port = port
        self.teardown = teardown
        time.sleep(10) # allows headles selenium to fully start
        self.driver = webdriver.Remote(command_executor=f"http://chromedriver:{self.port}/wd/hub", options=options)

    def land_coronavirus_data_website(self):
        """Nacigates to the goverment page from which tha data is being collected"""

        self.driver.get("https://wojewodztwa-rcb-gis.hub.arcgis.com/pages/dane-do-pobrania")

    def scrape_data(self):
        """Scrapes the data about Covid from the website"""

        wait = WebDriverWait(self.driver, 500)
        wait_unitl_link = wait.until(  # waits for the link to show up on the page
            EC.presence_of_element_located((
                By.XPATH, "//a[text() = 'Pobierz aktualne dane dla województw']"
            )))
        link = self.driver.find_element(
            By.LINK_TEXT,'Pobierz aktualne dane dla województw'
        )  # finds the link to data on page
        link_attribute = link.get_attribute('href')
        results = requests.get(link_attribute)
        results.encoding = 'WINDOWS-1250'
        results_text = results.text

        return results_text

    @staticmethod
    def create_dataframe(data):
        """Creates a dataframe from scraped data"""

        TESTDATA = StringIO(data)
        corona_df = pd.read_csv(TESTDATA, sep=';')

        return corona_df

    def __enter__(self):
        """Allows the usage of context menager"""

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Quits the browser if teardown is set to True"""

        if self.teardown:
            # shuts the page down after the search if selected to be True
            self.driver.close()
            self.driver.quit()
