from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from time import sleep
import os
import subprocess

def create_driver():
    options = Options()

    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # I am explictly passing geckodriver because I am using Python 3.14 and selenium doesn't really support it all that much
    # I am also sorry for this fuckass abomination of code that I have written
    service = Service(executable_path=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "geckodriver", "geckodriver.exe")))

    driver = webdriver.Firefox(service=service, options=options)
    return driver

def start_recording(driver):
    ffmpeg = subprocess.Popen([
        # I am sorry once more
        os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ffmpeg", "bin", "ffmpeg.exe")),
        "-y",
        "-f", "gdigrab",
        "-framerate", "30",
        "-i", "title=Mozilla Firefox",
        "-vcodec", "libx264",
        "-preset", "ultrafast",
        "video.mp4",
    ], stdin=subprocess.PIPE)

    sleep(2)
    return ffmpeg

def stop_recording(ffmpeg):
    ffmpeg.stdin.write(b"q")
    ffmpeg.stdin.flush()
    ffmpeg.wait()

def open_repo(driver, repo):
    driver.get(repo)
    # wait to load
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "article")))
    sleep(2)

def scroll_down(driver, pixels):
    current_scroll = 0
    speed = 100
    while current_scroll < pixels:
        driver.execute_script(f"window.scrollBy(0, {speed})")
        current_scroll += speed
        sleep(0.1)
    sleep((pixels/speed) * 0.1 + 1) # make sure the multiplier value is the same as the sleep value in the while loop!
    
def create_video(repo):
    driver = create_driver()
    ffmpeg = start_recording(driver)

    # proof video process
    open_repo(driver, repo)
    scroll_down(driver, 800)
    sleep(5)

    stop_recording(ffmpeg)
    driver.quit()

if __name__ == "__main__":
    create_video("https://github.com/utkrstht/clank")