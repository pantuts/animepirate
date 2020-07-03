#!/usr/bin/env python3

from animepirate.config import URLS_EP, VIDSOURCES_URL_FORMATS
from animepirate.utils import set_driver
import re


def ep_extractor(url):
    ep = None
    for k, v in URLS_EP.items():
        if k in url:
            if type(v) == tuple:
                ep = url.split(v[0])[-1].replace(v[1], '')
            else:
                ep = url.split(v)[-1]
            break
    return ep


class VideoParser:
    def __init__(self, url, from_episode=None, to_episode=None, is_movie=False):
        self.url = url
        self.from_episode = from_episode
        self.to_episode = to_episode
        self.is_movie = is_movie
        self.driver = set_driver()
        self.videos = []

    def parse(self):
        if self.to_episode:
            fr = 1 if not self.from_episode else int(self.from_episode)
            for i in range(fr, int(self.to_episode) + 1):
                self._parse(i)
        else:
            self._parse()

    def _parse(self, ep=None):
        url, vs = self._set_vidsources_parser(ep)
        vs.parse()
        video = vs.video
        if video:
            v = (url, video)
            self.videos.append(v)

    def _set_vidsources_parser(self, ep=None):
        url = ''
        vs = None
        for k, v in VIDSOURCES_URL_FORMATS.items():
            if k in self.url:
                if self.is_movie:
                    url = self.url
                else:
                    if not v.get('format2'):
                        url = v.get('format').format(self.url, str(ep)) if ep else self.url
                    else:
                        f2 = v.get('format2')
                        url = re.sub(v.get('regex'), f2.format(str(ep)), self.url) if ep else self.url

                if v.get('driver'):
                    vs = v.get('vs').VSParser(url, self.driver)
                else:
                    vs = v.get('vs').VSParser(url)
        return url, vs
