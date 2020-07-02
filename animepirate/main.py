#!/usr/bin/env python3

from animepirate.vidsources import twistmoe, animefreak
from animepirate.config import DRIVER_CACHE_FOLDER, VIDEOS_FOLDER
from animepirate.utils import set_driver, download, create_dir
import argparse
import sys


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

    create_dir(DRIVER_CACHE_FOLDER)
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
