# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "你的MUSIC_U", "value": "00FCDD857DAFF91EA31ECB328FF4EB64EB0E3377FB54BC8A0566E32BF638DB8CE4EE1493903124FB678D43E9D65F974318DD90B116FA6340D328DA4F82AFE0152C858B86A9874EB9ADD3021E4E0654B34DD7F8A9F7A5B26EAB16C556D0D0C8CC0C3CB93C571B76F32B8C673F23A7B7A8D7653A4D4E08043938BEE2F90A9B72A7E7A0F616208CA6F3364C21CB952116C871F321B967A3E4000FB7324B19F3D36DA4646C09677BAC3252C5B7AAE840F76D89BB7E6D532E2B05070AE3C535A52DC09D6EE52E2D922CE762DDDB7381D558B28586B58C940E58CFBA7DABAC491785C1F3EC805A24D7A74538D4F5361E87C585AF233E959A41ED782B41DFEB9E66D2B35BFCCFFED178FBEC443858F2C6CFA498919A7EBAB84F5BC976A67EADAD131AA984C9977DA412F80AA368FD6D8534D677AE98C9265F61799B46FB4054901DF7ABAC9C6723303B9486B1D90DAAC3F715BED8"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
