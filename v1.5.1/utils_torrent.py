import requests
from qbittorrent import Client


def download_torrent(url: str) -> None:
    """
    Function to download the torrent tile of a particular anime
    :param url: Url of the torrent file in the nyaa.si website.
    :return: None
    """
    r = requests.get(url, allow_redirects=True)
    file_name = re.findall("download/(.+)\.torrent", url)[0]
    open(f'{file_name}.torrent', 'wb').write(r.content)


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
