#!/usr/bin/env python3

from animepirate.config import DRIVER_CACHE_FOLDER
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from urllib.parse import unquote
import os
import platform
import requests


def set_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f'--disk-cache-dir={DRIVER_CACHE_FOLDER}')
    # disable images
    prefs = {}
    prefs["profile.default_content_settings"] = {"images": 2}
    prefs["profile.managed_default_content_settings"] = {"images": 2}
    prefs['disk-cache-size'] = 52428800
    options.experimental_options["prefs"] = prefs
    if platform.system() == 'Windows':
        driver = webdriver.Chrome(executable_path=f'{os.getenv("HOME")}/chromedriver.exe', options=options)
    else:
        driver = webdriver.Chrome(options=options)
    return driver


def create_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def download(ref, url, folder):
    fname = unquote(url).split('/')[-1].split('?')[0]
    if fname == 'video.mp4':
        fname = f'video-{ref.rpartition("/")[-1]}.mp4'
    fname = os.path.join(folder, fname)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'dnt': '1',
        'Host': list(filter(None, url.split('/')))[1],
        'Referer': ref,
        'Sec-Fetch-Dest': 'video',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    session = requests.Session()
    resp = session.get(url, headers=headers, stream=True, verify=False)
    try:
        with tqdm.wrapattr(open(fname, 'wb'), 'write',
                    miniters=1, desc=os.path.basename(fname),
                    total=int(resp.headers.get('content-length', 0))) as fout:
            for chunk in resp.iter_content(chunk_size=4096):
                fout.write(chunk)
    except Exception as e:
        print(e)
