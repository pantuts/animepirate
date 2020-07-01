#!/usr/bin/env python3

from animepirate.vidsources import twistmoe, animefreak

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from urllib.parse import unquote
import argparse
import math
import os
import platform
import random
import re
import requests
import sys
import time

CACHE_FOLDER = f'{os.getenv("HOME")}/.animepirate'
VIDEOS_FOLDER = f'{os.getenv("HOME")}/Desktop/animepirate-videos'


def create_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


def set_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f'--disk-cache-dir={CACHE_FOLDER}')
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


def download(ref, url, folder):
    fname = unquote(url).split('/')[-1].split('?')[0]
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
    resp = session.get(url, headers=headers, stream=True)
    try:
        with tqdm.wrapattr(open(fname, 'wb'), 'write',
                    miniters=1, desc=fname,
                    total=int(resp.headers.get('content-length', 0))) as fout:
            for chunk in resp.iter_content(chunk_size=4096):
                fout.write(chunk)
    except Exception as e:
        print(e)


def parse_video(url, from_episode=None, to_episode=None):
    videos = []

    driver = set_driver()

    if to_episode:
        fr = 1 if not from_episode else int(from_episode)
        for i in range(fr, int(to_episode) + 1):
            vs = None
            new_url = ''
            if 'twist.moe' in url:
                # url: https://twist.moe/a/kingdom/
                # needed: https://twist.moe/a/kingdom/{NUM}
                new_url = f'{url}{str(i)}'
                vs = twistmoe.TwistMoe(new_url, driver)
            elif 'animefreak.tv' in url or 'animefreak' in url:
                # url: https://www.animefreak.tv/watch/fruits-basket-2nd-season/
                # needed: https://www.animefreak.tv/watch/fruits-basket-2nd-season/episode/episode-{NUM}
                new_url = f'{url}episode/episode-{str(i)}'
                vs = animefreak.AnimeFreak(new_url)
            vs.parse()
            video = vs.video
            if video:
                v = (new_url, video)
                videos.append(v)
    else:
        vs = None
        if 'twist.moe' in url:
            vs = twistmoe.TwistMoe(url, driver)
        elif 'animefreak.tv' in url or 'animefreak' in url:
            vs = animefreak.AnimeFreak(url)
        vs.parse()
        video = vs.video
        if video:
            v = (url, video)
            videos.append(v)
    return videos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from-episode', help='Total episodes')
    parser.add_argument('-t', '--to-episode', help='To episode')
    parser.add_argument('-c', '--folder', help='Specify user output folder. Default is ~/Desktop.')
    parser.add_argument('-u', '--url', help='Url - with episode or none')
    args = parser.parse_args()
    from_ep = args.from_episode
    to_ep = args.to_episode
    url = args.url
    folder = args.folder if args.folder else VIDEOS_FOLDER

    create_dir(CACHE_FOLDER)
    create_dir(folder)

    if not url:
        parser.error('-u, --url is required')
    else:
        ep = None
        if 'twist.moe' in url:
            ep = url.split('/')[-1]
        elif 'animefreak.tv' in url or 'animefreak' in url:
            ep = url.split('-')[-1]

        videos = []
        if not ep.isnumeric() and not to_ep:
            parser.error('-t, --to-episode is required')
        else:
            videos = parse_video(url, from_ep, to_ep)

        for v in videos:
            download(v[0], v[1], folder)


if __name__ == "__main__":
    main()
