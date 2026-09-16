from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from time import sleep

def create_driver():
    options = Options()

    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    driver = webdriver.Firefox(options=options)
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
