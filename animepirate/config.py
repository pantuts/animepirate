#!/usr/bin/env python3

from animepirate.vidsources import (
    twistmoe,
    animefreak,
    gogoanime,
    nineanime
)
import os

DRIVER_CACHE_FOLDER = f'{os.getenv("HOME")}/.animepirate/cache'
VIDEOS_FOLDER = os.getcwd()
MAX_RETRIES = 3

URLS_EP = {
    'twist.moe': '/',
    'animefreak.tv': '-',
    'gogoanime': '-',
    '9anime-tv': ('episode-', '-english-sub')  # (for split, for replace)
}
VIDSOURCES_URL_FORMATS = {
    'twist.moe': {
        'format': '{}{}', # url, ep
        'driver': True,
        'vs': twistmoe
    },
    'animefreak.tv': {
        'format': '{}episode/episode-{}',
        'vs': animefreak
    },
    'gogoanime': {
        'format': '{}ep-{}',
        'driver': True,
        'vs': gogoanime
    },
    '9anime-tv': {
        'format': '{}',
        'format2': '-episode-{}-',
        'regex': '-episode-[0-9]{1,4}-',
        'driver': True,
        'vs': nineanime
    },
}
