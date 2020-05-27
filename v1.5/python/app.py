import os
import re
import ssl
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from qbittorrent import Client

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Constants
DATABASE_PATH = "resources/anime.txt"
HORRIBLE_SUBS_NYAA = "https://nyaa.si/?f=0&c=0_0&q=%5BHorribleSubs%5D"
# QBITTORENT_PATH = "C:\Program Files\qBittorrent\qbittorrent.exe"


def open_url(url: str) -> object:
    """
    A function that returns a Beautiful soup object after opening url.

    :param url: URL of the site we want to scrape
    :return: Beautiful soup object
    """
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")

    return soup


def find_total_pages(soup: object) -> int:
    """
    A function that returns the total number of pages in nyaa.si website.

    :param soup: Beautiful soup object of the website.
    :return: The total number of pages
    """
    pages = []
    soup = open_url(HORRIBLE_SUBS_NYAA)
    tags = soup('a')
    for tag in tags:
        if re.search("^[0-9]+$", tag.text):
            pages.append(tag.text)

    return int(pages[-1])


def get_all_anime(total_pages: int) -> list:
    """
    Get all the anime listed on all the pages of the website.

    :param total_pages: Total number of pages of HorribleSubs.
    :return: List containing the name and the torrent id of the episode.
                eg: [('[HorribleSubs] Tower of God - 08 [720p].mkv', '1249430')]
    """
    titles = []
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
        if anime in row[0]:
            temp = re.findall("\[HorribleSubs\] (.+?) - ([0-9]+?) \[720p\].mkv", row[0])
            remote_data.append((temp[0][0], int(temp[0][1]), row[1]))

    unwatched = []
    for row in remote_data:
        if row[1] > watched_ep:
            unwatched.append(row)

    return unwatched


def add_torrent(file_path: str) -> bool:
    """
    Function to add torrent file to qbittorrent app.
    :param file_path: Path to the downloaded torrent file.
    :return: None
    """
    # connect to the qbittorent Web UI
    try:
        qb = Client('http://127.0.0.1:8080/')
        torrent_file = open(file_path, 'rb')
        qb.download_from_file(torrent_file)
        return True
    except requests.exceptions.ConnectionError:
        print("qBittorrent app is not open.")
        return False


def download_torrent(url: str) -> None:
    """
    Function to download the torrent tile of a particular anime
    :param url: Url of the torrent file in the nyaa.si website.
    :return: None
    """
    r = requests.get(url, allow_redirects=True)
    file_name = re.findall("download/(.+)\.torrent", url)[0]
    open(f'{file_name}.torrent', 'wb').write(r.content)


def check_seasonal_anime(anime: str, all_anime: list) -> bool:
    """
    Function to check whether the anime is being aired this season.
    Horrible subs only keeps the torrent files of the anime in the current season only,
    on the nyaa.si website.
    :param anime: Name of the anime to check.
    :param all_anime: List of all the animes of the current season.
    :return: True if anime in the current season else False.
    """
    for seasonal_anime in all_anime:
        if anime in seasonal_anime[0]:
            return True
    return False


def add_anime(anime_name, episodes, current_episode_=0):
    """
    Function to add a new anime to the database /resources/anime.txt

    Args:
        anime_name (str): Name of the anime.
        episodes (int): Total episodes in the anime.
        current_episode_ (int) : Current episode count. Default is 0 for new anime.
    Returns:
        None
    """

    with open(DATABASE_PATH, "a") as file:
        file.writelines(f"{anime_name}~{current_episode_}~{episodes}\n")

    print(f"\nSuccess! Added {anime_name} to database\n\n")


def anime_exists(anime_name):
    """
    Function to check if the anime exists in the database or not

    Args:
        anime_name (str): Name of the anime.
    Returns:
        bool: True if the anime exists else False.
    """

    with open(DATABASE_PATH, "r") as file:
        for line in file:
            if anime_name in line.split("~")[0]:
                return True
    return False


def update_anime(anime_name, episode):
    """
    Function to update the episodes watched till now of the particular anime.

    Args:
         anime_name (str): Name of the anime.
         episode (int): The current episodes.
    Returns:
        None
    """
    anime_data = []  # Necessary line
    with open(DATABASE_PATH, "r") as file:
        anime_data = file.readlines()

    for idx, anime_ in enumerate(anime_data):
        line_list = anime_.split("~")
        if anime_name in line_list[0]:
            anime_full_name = line_list[0]
            anime_data[idx] = f"{line_list[0]}~{episode}~{line_list[2]}"
            break

    anime_data.sort()
    with open(DATABASE_PATH, "w") as file:
        file.writelines(anime_data)

    print(f"\nSuccess! Updated the episode count of {anime_full_name}!\n\n")


def anime_progress(anime_name):
    """
    Function to list the current progress of the anime.
    We read the data from the database.

    Args:
          anime_name (str): Name of the anime.
    Returns:
        (tuple): (Full name of anime, Current episode, Total episodes)
    """

    with open(DATABASE_PATH, "r") as file:
        for line in file:
            line_list = line.split("~")
            if anime_name in line_list[0]:
                return tuple([line_list[0], line_list[1], line_list[2].rstrip("\n")])


def anime_progress_all():
    """
    Function to list the current progress of the all the anime in the database.

    Args:
        No arguments
    Returns:
        tuple of tuples: Tuple of Tuples in the format ((anime-name, current-episode, total-episode))
    """
    all_anime_ = []
    with open(DATABASE_PATH, "r") as file:
        for line in file:
            line_list = line.split("~")
            all_anime_.append(tuple([line_list[0], line_list[1], line_list[2].rstrip("\n")]))
    return tuple(all_anime_)


def main():
    # Show initial progress
    print("\nCurrent Watch list:")
    print("-------------------\n")
    all_anime = anime_progress_all()
    if all_anime == ():
        print("You are watching no anime currently\n")
    else:
        for anime in all_anime:
            print(f"{anime[0]}: {anime[1]}/{anime[2]}\n", end="")
        print()

    scrape_flag = False
    qbittorent_flag = False
    all_anime = []
    while True:
        choice = input("""\nKon'nichiwa! Hajimemashite!
What do you want to do?
1. Add new anime
2. Update progress on existing anime
3. View progress on existing anime
4. All currently watching anime
5. Check for new episodes of a particular anime.
6. Check for new episodes of all currently watching anime.
7. Exit
Enter your choice:> """)

        if choice == "1":
            anime = input("Enter the name of the anime:> ")
            current_episode = int(input("Enter the current episode number:> "))
            total_episodes = int(input("Enter the total number of episodes:> "))

            if not anime_exists(anime):
                add_anime(anime, total_episodes, current_episode)
            else:
                print("Anime already exists")

        elif choice == "2":
            anime = input("Enter the name of the anime:> ")
            if anime_exists(anime):
                current_episode = int(input("Enter the current episode number:> "))
                update_anime(anime, current_episode)
            else:
                print("\nThe anime does not exist.\n")

        elif choice == "3":
            anime = input("Enter the name of the anime:> ")
            if anime_exists(anime):
                anime_full_name, current, total = anime_progress(anime)
                print("\nProgress:")
                print(f"{anime_full_name}: {current}/{total}\n")
            else:
                print("\nThe anime does not exist.\n")

        elif choice == "4":
            all_anime_ = anime_progress_all()
            if all_anime_ == ():
                print("You are watching no anime currently\n")
            else:
                print("\nCurrent Watch list:\n")
                for anime in all_anime_:
                    print(f"{anime[0]}: {anime[1]}/{anime[2]}\n", end="")
                print()

        elif choice == "5":
            # Code to start qbittorent in windows. Fix after learning concurrency.
            # if not qbittorent_flag:
            #     os.system(f'cmd /k "{QBITTORENT_PATH}"')
            #     qbittorent_flag = True

            if not scrape_flag:
                soup = open_url(HORRIBLE_SUBS_NYAA)
                print('Connection established to website')
                total_pages = find_total_pages(soup)
                print(f"Total pages of Horrible Subs in nyaa.si website: {total_pages}")
                all_anime = get_all_anime(total_pages)
                scrape_flag = True

            anime = input("Enter the name of the anime:> ")
            if anime_exists(anime):
                if check_seasonal_anime(anime, all_anime):
                    current_progress = anime_progress(anime)

                    unwatched_episodes = track_anime(current_progress[0], int(current_progress[1]), all_anime)

                    if len(unwatched_episodes) == 0:
                        print("You are up to date!")
                    else:
                        print(f"You have {len(unwatched_episodes)} episodes to watch.")
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
                else:
                    print("The anime is not being aired this season.")
            else:
                print("\nAnime does not exist")

        elif choice == "6":
            # Code to start qbittorent in windows. Fix after learning concurrency.
            # if not qbittorent_flag:
            #     os.system(f'cmd /k "{QBITTORENT_PATH}"')
            #     qbittorent_flag = True
            # Code to scrape
            if not scrape_flag:
                soup = open_url(HORRIBLE_SUBS_NYAA)
                print('Connection established to website')
                total_pages = find_total_pages(soup)
                print(f"Total pages of Horrible Subs in nyaa.si website: {total_pages}")
                all_anime = get_all_anime(total_pages)
                scrape_flag = True

            all_current_anime = anime_progress_all()
            for anime in all_current_anime:
                if check_seasonal_anime(anime[0], all_anime):
                    unwatched_episodes = track_anime(anime[0], int(anime[1]), all_anime)

                    if len(unwatched_episodes) == 0:
                        print(f"\nYou are up to date in {anime[0]}!")
                    else:
                        print(f"\nYou have {len(unwatched_episodes)} episodes to watch in {anime[0]}.")
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
                else:
                    print(f"\n{anime[0]} is not this season's anime!")

            print("\nChecked all anime!")

        elif choice == "7":
            break

        else:
            print("Invalid input\n")


if __name__ == '__main__':
    main()
