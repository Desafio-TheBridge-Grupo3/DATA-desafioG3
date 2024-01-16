from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

import time
from dotenv import load_dotenv
import os

load_dotenv()
URL =  os.getenv("URL")
USER =  os.getenv("USER")
PASSWORD =  os.getenv("PASSWORD")

def get_soup_info(driver):
    """
    Extract information from a web page using Selenium WebDriver.

    Args:
        driver: Selenium WebDriver instance.

    Returns:
        dict: Extracted information for candelas web.
    """
    candela_info = {
        "rate": [],
        "anual_consumption": [],
        "anual_consumption_p1": [],
        "anual_consumption_p2": [],
        "anual_consumption_p3": [],
        "anual_consumption_p4": [],
        "anual_consumption_p5": [],
        "anual_consumption_p6": [],
        "anual_power_p1": [],
        "anual_power_p2": [],
        "anual_power_p3": [],
        "anual_power_p4": [],
        "anual_power_p5": [],
        "anual_power_p6": []
    }

    candela_info["rate"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[9]').text
    candela_info["anual_consumption"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[11]').text
    candela_info["anual_consumption_p1"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[13]').text
    candela_info["anual_consumption_p2"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[14]').text
    candela_info["anual_consumption_p3"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[15]').text
    candela_info["anual_consumption_p4"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[16]').text
    candela_info["anual_consumption_p5"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[17]').text
    candela_info["anual_consumption_p6"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[18]').text
    candela_info["anual_power_p1"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[21]').text
    candela_info["anual_power_p2"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[22]').text
    candela_info["anual_power_p3"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[23]').text
    candela_info["anual_power_p4"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[24]').text
    candela_info["anual_power_p5"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[25]').text
    candela_info["anual_power_p6"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[26]').text

    return candela_info

def webscraping_chrome_candelas(cups):
    """
    Perform web scraping on the Candela website to retrieve information.

    Args:
        cups (str): The CUPS identifier.

    Returns:
        dict: Extracted information including rate, annual_consumption, annual_consumption_p1,
              annual_consumption_p2, annual_consumption_p3, annual_consumption_p4,
              annual_consumption_p5, annual_consumption_p6, annual_power_p1,
              annual_power_p2, annual_power_p3, annual_power_p4, annual_power_p5,
              annual_power_p6.
    """
    try:
        path_driver = os.getcwd() + "\webscraping\chromedriver-win64\chromedriver.exe"
        # Create driver Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")

        service = Service(path_driver)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(URL)
        assert "Candela"
        time.sleep(5)

        # Login in candelas web

        driver.find_element(By.ID, "select_1").click()
        time.sleep(2)
        driver.find_element(By.ID, "select_option_3").click()
        driver.find_element(By.NAME, "usuario").send_keys(USER)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form/button').click()
        time.sleep(10)

        # Download info

        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[1]/ul/li[3]/a').click()
        time.sleep(1)
        driver.find_element(By.ID, "input_6").send_keys(cups)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-card/div[1]/form/div[4]/button').click()
        time.sleep(10)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-toolbar/div[1]/button[1]').click()

        info = get_soup_info(driver)

        # Close driver
        driver.quit()
        return info
    except Exception as e:
        return {"error": str(e)}


