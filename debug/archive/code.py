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


def main():
    HORRIBLE_SUBS_NYAA = "https://nyaa.si/?f=0&c=0_0&q=%5BHorribleSubs%5D"

    soup = open_url(HORRIBLE_SUBS_NYAA)
    print('Connection established to website')
    # total_pages = find_total_pages(soup)
    total_pages = 14
    print(f"Total pages of Horrible Subs: {total_pages}")

    all_anime = get_all_anime(total_pages)
    track_anime("Kakushigoto", 6, all_anime)


if __name__ == '__main__':
    pass
