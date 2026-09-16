from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from time import sleep
import os

def create_driver():
    options = Options()

    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # I am explictly passing geckodriver because I am using Python 3.14 and selenium doesn't really support it all that much
    # I am also sorry for this fuckass abomination of code that I have written
    service = Service(executable_path=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "geckodriver", "geckodriver.exe")))

    driver = webdriver.Firefox(service=service, options=options)
    return driver

def open_repo(driver, repo):
    driver.get(repo)
    # wait to load
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "article")))
    sleep(2)

def scroll_down(driver, pixels):
    driver.execute_script(f"window.scrollBy(0, {pixels})")
    sleep(1)

def create_video(repo):
    driver = create_driver()

    # proof video process
    open_repo(driver, repo)
    scroll_down(driver)
    sleep(5)

    driver.quit()
