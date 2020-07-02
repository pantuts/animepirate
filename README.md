# animepirate

Dumb anime videos downloader. Too dumb, yes!

Currently supports:
1. AnimeFreak
2. TwistMoe

Todos:
1. Add more sites.
2. Logger

## Windows

!Note: Haven't tested this, i don't have a windows installed.

Download `chromedriver` here [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads), extract, and then put `chromedriver.exe` to your home directory. Make sure you download version that corresponds to your current install Chrome/Chromium.

## Nix

Just install `chromedriver`from your favorite package manager.

## Install

```
git clone https://github.com/pantuts/animepirate
cd animepirate
pip install -r requirements.txt
python setup.py build
sudo python setup.py install
```

## Usage

```
pirateanime -u URL -f 2 -t 3    # from episode 2 - 3
pirateanime -u URL -t 3         # will start from 1 up to 3
pirateanime -u URL -t 3 -c ~/Desktop/test   # save videos to ~/Desktop/test
pirateanime -u URL # will download specific episode if detected
```

## Agreement

By using this software, you agree that you and you alone will be held liable for any damage you may accidentally do to supported sites. This is for educational purposes only.
