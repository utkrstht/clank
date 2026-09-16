from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from time import sleep
from utils import get_repository_default_branch, get_repository_tree
from checks import source_extensions
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

def open_file(driver, filepath):
    repo = driver.current_url.rstrip("/")

    if "/blob/" in repo or "/tree/" in repo:
        repo = repo.split("/blob/")[0].split("/tree/")[0]

    driver.get(f"{repo}/blob/main/{filepath}")
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    sleep(2)


def scroll(driver, direction, pixels):
    current_scroll = 0
    speed = 250 if direction == "down" else -250
    while current_scroll < pixels:
        driver.execute_script(f"window.scrollBy(0, {speed})")
        current_scroll += 250
        sleep(0.01)
    sleep((pixels/speed) * 0.1 + 1) # make sure the multiplier value is the same as the sleep value in the while loop!

def high_scroll(driver, direction):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        if direction == "down":
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
            sleep(1)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        else:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
            sleep(1)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height            
    
def create_video(repo, stardance, demo):
    driver = create_driver()
    ffmpeg = start_recording(driver.title)

    api_repo = repo.replace("https://github.com/", "https://api.github.com/repos/")

    # obtain repository files
    branch = get_repository_default_branch(api_repo, {})
    tree = get_repository_tree(api_repo, branch, {})

    source_files = [ item for item in tree if item["type"] == "blob" and item["path"].endswith(source_extensions) ]

    # proof video process
    open_url(driver, stardance)
    sleep(3)
    open_url(driver, demo)
    high_scroll(driver, "down")
    high_scroll(driver, "up")
    sleep(2)
    open_url(driver, repo)
    sleep(3)

    # open all source files 
    for file in source_files:
        path = file["path"]

        try:
           open_file(driver, file["path"])

           total_height = driver.execute_script("return document.documentElement.scrollHeight") 

           high_scroll(driver, "down")
           high_scroll(driver, "up") 
           #scroll(driver, "down", total_height)
           #scroll(driver, "up", total_height)
        except Exception as e:
            print(f"yikes (could not open {path}): {e}")    

    stop_recording(ffmpeg)
    driver.quit()

if __name__ == "__main__":
    create_video("https://github.com/utkrstht/clank", "https://stardance.hackclub.com/projects/49970", "https://github.com/utkrstht")