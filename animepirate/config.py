#!/usr/bin/env python3

from animepirate.vidsources import twistmoe, animefreak
import os

DRIVER_CACHE_FOLDER = f'{os.getenv("HOME")}/.animepirate/cache'
VIDEOS_FOLDER =  os.getcwd()

URLS_EP = {
    'twist.moe': '/',
    'animefreak.tv': '-'
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
    }
}
