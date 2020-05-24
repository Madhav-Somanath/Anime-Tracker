import ssl
import re
import requests
from urllib.request import urlopen
from qbittorrent import Client
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Constants
DATABASE_PATH = "resources/anime.txt"
HORRIBLE_SUBS_NYAA = "https://nyaa.si/?f=0&c=0_0&q=%5BHorribleSubs%5D"


# new
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
    container = soup.find('ul', class_="pagination")
    pages = []
    for tag in container.find_all("li"):
        pages.append(tag.text)

    return int(pages[-2])


def get_all_anime(total_pages: int) -> list:
    """
    Get all the anime listed on all the pages of the website.

    :param total_pages: Total number of pages of HorribleSubs.
    :return: List containing the names of all the anime.
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
    """
    remote_data = []
    for row in all_anime:
        if anime in row[0]:
            temp = re.findall("\[HorribleSubs\] ([a-zA-Z]+?) - ([0-9]+?) \[720p\].mkv", row[0])
            remote_data.append((temp[0][0], int(temp[0][1]), row[1]))

    unwatched = []
    for row in remote_data:
        if row[1] > watched_ep:
            unwatched.append(row)

    return unwatched


def add_torrent(file_path: str) -> None:
    """
    Function to add torrent file to qbittorrent app.
    :param file_path: Path to the downloaded torrent file.
    :return: None
    """
    # connect to the qbittorent Web UI
    try:
        qb = Client('https://127.0.0.1:8080/')
        torrent_file = open(file_path, 'rb')
        qb.download_from_file(torrent_file)
        print("Torrent added. Starting download.")
    except requests.exceptions.ConnectionError:
        print("qBittorrent app is not open.")


def download_torrent(url: str) -> None:
    """
    Function to download the torrent tile of a particular anime
    :param url: Url of the torrent file in the nyaa.si website.
    :return: None
    """
    r = requests.get(url, allow_redirects=True)
    file_name = re.findall("download/(.+)\.torrent", url)[0]
    print(file_name)
    open(f'{file_name}.torrent', 'wb').write(r.content)


# old
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
    while True:
        choice = input("""Kon'nichiwa! Hajimemashite!
What do you want to do?
1. Add new anime
2. Update progress on existing anime
3. View progress on existing anime
4. All currently watching anime
5. Exit
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
            if all_anime == ():
                print("You are watching no anime currently\n")
            else:
                print("\nCurrent Watch list:\n")
                for anime in all_anime_:
                    print(f"{anime[0]}: {anime[1]}/{anime[2]}\n", end="")
                print()
        elif choice == "5":
            break
        else:
            print("Invalid input\n")


if __name__ == '__main__':
    print("Current Watch list:\n")
    all_anime = anime_progress_all()
    if all_anime == ():
        print("You are watching no anime currently\n")
    else:
        for anime in all_anime:
            print(f"{anime[0]}: {anime[1]}/{anime[2]}\n", end="")
        print()

    main()
