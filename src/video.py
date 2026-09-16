from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from time import sleep
import os
import subprocess
import signal

def create_driver():
    options = Options()

    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # I am explictly passing geckodriver because I am using Python 3.14 and selenium doesn't really support it all that much
    # I am also sorry for this fuckass abomination of code that I have written
    service = Service(executable_path=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "geckodriver", "geckodriver.exe")))

    driver = webdriver.Firefox(service=service, options=options)
    return driver

def start_recording(window):
    ffmpeg = subprocess.Popen([
        # I am sorry once more
        os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ffmpeg", "bin", "ffmpeg.exe")),
        "-y",
        "-f", "gdigrab",
        "-framerate", "30",
        "-i", "desktop",
        "-c:v", "mpeg4",
        "-q:v", "5",
        "video.avi",
    ], stdin=subprocess.PIPE)

    sleep(2)
    return ffmpeg

def stop_recording(ffmpeg):
    ffmpeg.stdin.write(b"q")
    ffmpeg.stdin.flush()
    ffmpeg.wait()

def open_url(driver, url):
    driver.get(url)
    # wait to load
    WebDriverWait(driver, 10).until(
        # check if basic html body is loaded
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    sleep(2)

def scroll_down(driver, pixels):
    current_scroll = 0
    speed = 100
    while current_scroll < pixels:
        driver.execute_script(f"window.scrollBy(0, {speed})")
        current_scroll += speed
        sleep(0.1)
    sleep((pixels/speed) * 0.1 + 1) # make sure the multiplier value is the same as the sleep value in the while loop!
    
def create_video(repo, stardance, demo):
    driver = create_driver()
    ffmpeg = start_recording(driver.title)

    # proof video process
    open_url(driver, stardance)
    sleep(3)
    open_url(driver, demo)
    scroll_down(driver, 1000)
    sleep(2)
    open_url(driver, repo)
    sleep(3)

    stop_recording(ffmpeg)
    driver.quit()

if __name__ == "__main__":
    create_video("https://github.com/utkrstht/clank", "https://stardance.hackclub.com/projects/49970", "https://github.com/utkrstht")