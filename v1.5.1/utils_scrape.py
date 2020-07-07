import os
import ssl
from urllib.request import urlopen

from bs4 import BeautifulSoup

from utils_anime import get_all_anime
from utils_torrent import *

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Constants
DATABASE_PATH = "resources/anime.txt"
HORRIBLE_SUBS_NYAA = "https://nyaa.si/?f=0&c=0_0&q=%5BHorribleSubs%5D"
TOTAL_PAGES = 14


def open_url(url: str) -> object:
    """
    A function that returns a Beautiful soup object after opening url.

    :param url: URL of the site we want to scrape
    :return: Beautiful soup object
    """
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    return soup


def scrape_data() -> list:
    """
    Get all the anime listed on all the pages of the website.

    :return: List containing the name and the torrent id of the episode.
                eg: [('[HorribleSubs] Tower of God - 08 [720p].mkv', '1249430')]
    """
    total_pages = TOTAL_PAGES
    titles = []

    print("Connected to website")
    for page in range(1, total_pages + 1):
        print(f"Processing page: {page}/{total_pages}")
        url = f"https://nyaa.si/?f=0&c=0_0&q=[HorribleSubs]&p={page}"
        soup = open_url(url)
        tags = soup('a')
        for tag in tags:
            anime_id = tag.get('href', None)
            temp = tag.get('title', None)
            if temp and temp.startswith("[HorribleSubs]") and temp.endswith("[720p].mkv"):
                anime_id = re.findall("view/([0-9]+)", anime_id)[0]
                # temp = re.findall("\[HorribleSubs\] (.*?) - ([0-9]*) \[720p\].mkv", temp)
                titles.append((temp, anime_id))
    print("Done!")
    print("Anime retrieval complete!")
    return titles


def track_anime(anime: str, watched_ep: int, all_anime: list) -> list:
    """
    A function to find all the released episode of a particular anime.

    :param anime: The name of the anime we have to track.
    :param watched_ep: The last watched episode number
    :param all_anime: List of all the animes that are released.
    :return: List containing all the unwatched episodes of a particular anime.
                eg: [('Gleipnir', 8, '1249430')]    # where 1249430 is the torrent id
    """

    remote_data = []
    for row in all_anime:
        if anime.lower().replace(" ", "") in row[0].lower().replace(" ", ""):
            temp = re.findall("\[HorribleSubs\] (.+?) - ([0-9]+?) \[720p\].mkv", row[0])
            remote_data.append((temp[0][0], int(temp[0][1]), row[1]))

    unwatched = []
    for row in remote_data:
        if row[1] > watched_ep:
            unwatched.append(row)

    return unwatched


def check_new_episodes(all_anime):
    all_current_anime = get_all_anime()
    for anime in all_current_anime:
        unwatched_episodes = track_anime(anime[1], int(anime[2]), all_anime)

        if len(unwatched_episodes) == 0:
            print(f"\nYou are up to date in {anime[1]}!")
        else:
            print(f"\nYou have {len(unwatched_episodes)} episodes to watch in {anime[1]}.")
            download_prompt = input("Download and add to qBittorrent? Yes/No:> ")
            if download_prompt.lower() == "yes":
                for row in unwatched_episodes:
                    download_torrent(f"https://nyaa.si/download/{row[-1]}.torrent")
                    print(f"Downloaded {row[0]} Episode: {row[1]}")
                    if add_torrent(f"{row[-1]}.torrent"):
                        print("Torrent added. Starting download.\n")
                    else:
                        print("Couldn't add torrent!")
                    os.remove(f"{row[-1]}.torrent")
            else:
                print("\nOkay!")
