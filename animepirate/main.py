#!/usr/bin/env python3

from animepirate.config import DRIVER_CACHE_FOLDER, VIDEOS_FOLDER
from animepirate.parser import VideoParser, ep_extractor
from animepirate.utils import download, create_dir
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from-episode', help='Total episodes')
    parser.add_argument('-t', '--to-episode', help='To episode')
    parser.add_argument('-c', '--folder', help='Specify user output folder. Default is ~/Desktop.')
    parser.add_argument('-m', '--movie', help='Required if a movie.', action='store_true')
    parser.add_argument('-g', '--gui', help='Run headless (default) or gui.', action='store_false')
    parser.add_argument('-u', '--url', help='Url - with episode or none')
    args = parser.parse_args()
    from_ep = args.from_episode
    to_ep = args.to_episode
    is_movie = args.movie
    gui = args.gui
    url = args.url
    folder = args.folder if args.folder else VIDEOS_FOLDER

    create_dir(DRIVER_CACHE_FOLDER)
    create_dir(folder)

    if not url:
        parser.error('-u, --url is required')
    else:
        ep = ep_extractor(url)
        videos = []

        # means ep is not included in url
        if not ep.isnumeric() and not to_ep and not is_movie:
            parser.error('-t, --to-episode is required')
        else:
            vp = VideoParser(url, from_ep, to_ep, is_movie, gui)
            vp.parse()
            videos = vp.videos

        for v in videos:
            download(v[0], v[1], folder)


if __name__ == "__main__":
    main()
