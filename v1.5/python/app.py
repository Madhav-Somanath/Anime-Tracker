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
    # For testing:
    # return [('[HorribleSubs] Gleipnir - 08 [720p].mkv', '1249430'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 08 [720p].mkv', '1249405'),
    #         ('[HorribleSubs] Tsugumomo S2 - 08 [720p].mkv', '1249379'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 22 [720p].mkv', '1249160'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 08 [720p].mkv', '1249127'),
    #         ('[HorribleSubs] Hamefura - 08 [720p].mkv', '1249107'),
    #         ('[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 07 [720p].mkv', '1249076'),
    #         ('[HorribleSubs] Arte - 08 [720p].mkv', '1249057'), ('[HorribleSubs] Listeners - 08 [720p].mkv', '1248860'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 08 [720p].mkv', '1248858'),
    #         ('[HorribleSubs] Bungo to Alchemist - Shinpan no Haguruma - 06 [720p].mkv', '1248839'),
    #         ('[HorribleSubs] Toaru Kagaku no Railgun T - 15 [720p].mkv', '1248797'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 08 [720p].mkv', '1248771'),
    #         ('[HorribleSubs] Zashiki Warashi no Tatami-chan - 07 [720p].mkv', '1248731'),
    #         ('[HorribleSubs] Kakushigoto - 08 [720p].mkv', '1248539'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 08 [720p].mkv', '1248518'),
    #         ('[HorribleSubs] Plunderer - 19 [720p].mkv', '1248287'),
    #         ('[HorribleSubs] Tower of God - 08 [720p].mkv', '1248235'),
    #         ('[HorribleSubs] Tamayomi - 08 [720p].mkv', '1248226'),
    #         ('[HorribleSubs] Ahiru no Sora - 32 [720p].mkv', '1248190'),
    #         ('[HorribleSubs] Shadowverse - 07 [720p].mkv', '1247973'),
    #         ('[HorribleSubs] A3! Season Spring & Summer - 07 [720p].mkv', '1247821'),
    #         ('[HorribleSubs] Fruits Basket S2 (2019) - 07 [720p].mkv', '1247787'),
    #         ('[HorribleSubs] Princess Connect! Re Dive - 07 [720p].mkv', '1247770'),
    #         ('[HorribleSubs] Kitsutsuki Tanteidokoro - 06 [720p].mkv', '1247746'),
    #         ('[HorribleSubs] Shironeko Project - Zero Chronicle - 07 [720p].mkv', '1247730'),
    #         ('[HorribleSubs] Gleipnir - 07 [720p].mkv', '1247521'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 07 [720p].mkv', '1247494'),
    #         ('[HorribleSubs] Tsugumomo S2 - 07 [720p].mkv', '1247480'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 21 [720p].mkv', '1247261'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 07 [720p].mkv', '1247235'),
    #         ('[HorribleSubs] Gal to Kyouryuu - 07 [720p].mkv', '1247221'),
    #         ('[HorribleSubs] Hamefura - 07 [720p].mkv', '1247220'),
    #         ('[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 06 [720p].mkv', '1247190'),
    #         ('[HorribleSubs] Arte - 07 [720p].mkv', '1247162'), ('[HorribleSubs] Listeners - 07 [720p].mkv', '1246943'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 07 [720p].mkv', '1246934'),
    #         ('[HorribleSubs] Bungo to Alchemist - Shinpan no Haguruma - 05 [720p].mkv', '1246913'),
    #         ('[HorribleSubs] Toaru Kagaku no Railgun T - 14 [720p].mkv', '1246888'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 07 [720p].mkv', '1246872'),
    #         ('[HorribleSubs] Zashiki Warashi no Tatami-chan - 06 [720p].mkv', '1246843'),
    #         ('[HorribleSubs] Kakushigoto - 07 [720p].mkv', '1246648'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 07 [720p].mkv', '1246623'),
    #         ('[HorribleSubs] Plunderer - 18 [720p].mkv', '1246457'),
    #         ('[HorribleSubs] Tower of God - 07 [720p].mkv', '1246410'),
    #         ('[HorribleSubs] Tamayomi - 07 [720p].mkv', '1246401'),
    #         ('[HorribleSubs] Ahiru no Sora - 31 [720p].mkv', '1246352'),
    #         ('[HorribleSubs] Shadowverse - 06 [720p].mkv', '1246111'),
    #         ('[HorribleSubs] A3! Season Spring & Summer - 06 [720p].mkv', '1246029'),
    #         ('[HorribleSubs] Fruits Basket S2 (2019) - 06 [720p].mkv', '1245991'),
    #         ('[HorribleSubs] Princess Connect! Re Dive - 06 [720p].mkv', '1245973'),
    #         ('[HorribleSubs] Kitsutsuki Tanteidokoro - 05 [720p].mkv', '1245937'),
    #         ('[HorribleSubs] Shironeko Project - Zero Chronicle - 06 [720p].mkv', '1245929'),
    #         ('[HorribleSubs] Gleipnir - 06 [720p].mkv', '1245695'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 06 [720p].mkv', '1245678'),
    #         ('[HorribleSubs] Tsugumomo S2 - 06 [720p].mkv', '1245664'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 20 [720p].mkv', '1245408'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 06 [720p].mkv', '1245387'),
    #         ('[HorribleSubs] Gal to Kyouryuu - 06 [720p].mkv', '1245373'),
    #         ('[HorribleSubs] Hamefura - 06 [720p].mkv', '1245369'),
    #         ('[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 05 [720p].mkv', '1245344'),
    #         ('[HorribleSubs] Arte - 06 [720p].mkv', '1245332'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 06 [720p].mkv', '1245112'),
    #         ('[HorribleSubs] Listeners - 06 [720p].mkv', '1245094'),
    #         ('[HorribleSubs] Bungo to Alchemist - Shinpan no Haguruma - 04 [720p].mkv', '1245084'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 06 [720p].mkv', '1245024'),
    #         ('[HorribleSubs] Zashiki Warashi no Tatami-chan - 05 [720p].mkv', '1244982'),
    #         ('[HorribleSubs] Tamayomi - 04v2 [720p].mkv', '1244891'),
    #         ('[HorribleSubs] Kakushigoto - 06 [720p].mkv', '1244786'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 06 [720p].mkv', '1244763'),
    #         ('[HorribleSubs] Gundam Build Divers Re-RISE - 18 [720p].mkv', '1244739'),
    #         ('[HorribleSubs] Plunderer - 17 [720p].mkv', '1244598'),
    #         ('[HorribleSubs] Tower of God - 06 [720p].mkv', '1244554'),
    #         ('[HorribleSubs] Tamayomi - 06 [720p].mkv', '1244543'),
    #         ('[HorribleSubs] Ahiru no Sora - 30 [720p].mkv', '1244511'),
    #         ('[HorribleSubs] Shadowverse - 05 [720p].mkv', '1244311'),
    #         ('[HorribleSubs] A3! Season Spring & Summer - 05 [720p].mkv', '1244214'),
    #         ('[HorribleSubs] Fruits Basket S2 (2019) - 05 [720p].mkv', '1244174'),
    #         ('[HorribleSubs] Princess Connect! Re Dive - 05 [720p].mkv', '1244158'),
    #         ('[HorribleSubs] Kitsutsuki Tanteidokoro - 04 [720p].mkv', '1244116'),
    #         ('[HorribleSubs] Shironeko Project - Zero Chronicle - 05 [720p].mkv', '1244110'),
    #         ('[HorribleSubs] Gleipnir - 05 [720p].mkv', '1243876'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 05 [720p].mkv', '1243849'),
    #         ('[HorribleSubs] Tsugumomo S2 - 05 [720p].mkv', '1243837'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 19 [720p].mkv', '1243599'),
    #         ('[HorribleSubs] Hamefura - 05 [720p].mkv', '1243581'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 05 [720p].mkv', '1243568'),
    #         ('[HorribleSubs] Gal to Kyouryuu - 05 [720p].mkv', '1243550'),
    #         ('[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 04 [720p].mkv', '1243526'),
    #         ('[HorribleSubs] Arte - 05 [720p].mkv', '1243509'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 05 [720p].mkv', '1243330'),
    #         ('[HorribleSubs] Listeners - 05 [720p].mkv', '1243316'),
    #         ('[HorribleSubs] Toaru Kagaku no Railgun T - 13 [720p].mkv', '1243265'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 05 [720p].mkv', '1243230'),
    #         ('[HorribleSubs] Zashiki Warashi no Tatami-chan - 04 [720p].mkv', '1243196'),
    #         ('[HorribleSubs] Kakushigoto - 05 [720p].mkv', '1243001'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 05 [720p].mkv', '1242977'),
    #         ('[HorribleSubs] Gundam Build Divers Re-RISE - 17 [720p].mkv', '1242953'),
    #         ('[HorribleSubs] Plunderer - 16 [720p].mkv', '1242791'),
    #         ('[HorribleSubs] Tower of God - 05 [720p].mkv', '1242748'),
    #         ('[HorribleSubs] Tamayomi - 05 [720p].mkv', '1242743'),
    #         ('[HorribleSubs] Ahiru no Sora - 29 [720p].mkv', '1242699'),
    #         ('[HorribleSubs] Black Clover - 132 [720p].mkv', '1242419'),
    #         ('[HorribleSubs] Shadowverse - 04 [720p].mkv', '1242409'),
    #         ('[HorribleSubs] A3! Season Spring & Summer - 04 [720p].mkv', '1242299'),
    #         ('[HorribleSubs] Fruits Basket S2 (2019) - 04 [720p].mkv', '1242267'),
    #         ('[HorribleSubs] Princess Connect! Re Dive - 04 [720p].mkv', '1242237'),
    #         ('[HorribleSubs] Kitsutsuki Tanteidokoro - 03 [720p].mkv', '1242216'),
    #         ('[HorribleSubs] Shironeko Project - Zero Chronicle - 04 [720p].mkv', '1242199'),
    #         ('[HorribleSubs] Kingdom S3 - 04 [720p].mkv', '1241997'),
    #         ('[HorribleSubs] Gleipnir - 04 [720p].mkv', '1241916'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 04 [720p].mkv', '1241897'),
    #         ('[HorribleSubs] Tsugumomo S2 - 04 [720p].mkv', '1241865'),
    #         ('[HorribleSubs] Boruto - Naruto Next Generations - 154 [720p].mkv', '1241803'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 18 [720p].mkv', '1241653'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 04 [720p].mkv', '1241635'),
    #         ('[HorribleSubs] Gal to Kyouryuu - 04 [720p].mkv', '1241612'),
    #         ('[HorribleSubs] Hamefura - 04 [720p].mkv', '1241610'),
    #         ('[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 03 [720p].mkv', '1241587'),
    #         ('[HorribleSubs] Arte - 04 [720p].mkv', '1241552'),
    #         ('[HorribleSubs] Major 2nd S2 - 04 [720p].mkv', '1241486'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 04 [720p].mkv', '1241309'),
    #         ('[HorribleSubs] Listeners - 04 [720p].mkv', '1241300'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 04 [720p].mkv', '1241181'),
    #         ('[HorribleSubs] Appare-Ranman! - 03 [720p].mkv', '1241151'),
    #         ('[HorribleSubs] Zashiki Warashi no Tatami-chan - 03 [720p].mkv', '1241105'),
    #         ('[HorribleSubs] Kakushigoto - 04 [720p].mkv', '1240919'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 04 [720p].mkv', '1240893'),
    #         ('[HorribleSubs] Gundam Build Divers Re-RISE - 16 [720p].mkv', '1240857'),
    #         ('[HorribleSubs] Plunderer - 15 [720p].mkv', '1240681'),
    #         ('[HorribleSubs] Tower of God - 04 [720p].mkv', '1240663'),
    #         ('[HorribleSubs] Ahiru no Sora - 28 [720p].mkv', '1240604'),
    #         ('[HorribleSubs] Houkago Teibou Nisshi - 03 [720p].mkv', '1240397'),
    #         ('[HorribleSubs] Black Clover - 131 [720p].mkv', '1240356'),
    #         ('[HorribleSubs] Shadowverse - 03 [720p].mkv', '1240348'),
    #         ('[HorribleSubs] Kitsutsuki Tanteidokoro - 02 [720p].mkv', '1240226'),
    #         ('[HorribleSubs] Fruits Basket S2 (2019) - 03 [720p].mkv', '1240170'),
    #         ('[HorribleSubs] Princess Connect! Re Dive - 03 [720p].mkv', '1240145'),
    #         ('[HorribleSubs] Shironeko Project - Zero Chronicle - 03 [720p].mkv', '1240100'),
    #         ('[HorribleSubs] Kingdom S3 - 03 [720p].mkv', '1239896'),
    #         ('[HorribleSubs] Gleipnir - 03 [720p].mkv', '1239835'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 03 [720p].mkv', '1239818'),
    #         ('[HorribleSubs] IDOLiSH7 S2 - 04 [720p].mkv', '1239801'),
    #         ('[HorribleSubs] Tsugumomo S2 - 03 [720p].mkv', '1239792'),
    #         ('[HorribleSubs] Boruto - Naruto Next Generations - 153 [720p].mkv', '1239726'),
    #         ('[HorribleSubs] Digimon Adventure (2020) - 03 [720p].mkv', '1239642'),
    #         ('[HorribleSubs] One Piece - 929 [720p].mkv', '1239634'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 17 [720p].mkv', '1239538'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 03 [720p].mkv', '1239514'),
    #         ('[HorribleSubs] Gal to Kyouryuu - 03 [720p].mkv', '1239502'),
    #         ('[HorribleSubs] Hamefura - 03 [720p].mkv', '1239500'),
    #         ('[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 02 [720p].mkv', '1239472'),
    #         ('[HorribleSubs] Arte - 03 [720p].mkv', '1239446'),
    #         ('[HorribleSubs] Major 2nd S2 - 03 [720p].mkv', '1239390'),
    #         ('[HorribleSubs] Zashiki Warashi no Tatami-chan - 02 [720p].mkv', '1239278'),
    #         ('[HorribleSubs] Toaru Kagaku no Railgun T - 12 [720p].mkv', '1239276'),
    #         ('[HorribleSubs] Shokugeki no Soma S5 - 02 [720p].mkv', '1239272'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 03 [720p].mkv', '1239205'),
    #         ('[HorribleSubs] Gal to Kyouryuu - 02 [720p].mkv', '1239202'),
    #         ('[HorribleSubs] Listeners - 03 [720p].mkv', '1239199'),
    #         ('[HorribleSubs] Bungo to Alchemist - Shinpan no Haguruma - 03 [720p].mkv', '1239177'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 03 [720p].mkv', '1239121'),
    #         ('[HorribleSubs] Appare-Ranman! - 02 [720p].mkv', '1239113'),
    #         ('[HorribleSubs] Fugou Keiji Balance - UNLIMITED - 02 [720p].mkv', '1238899'),
    #         ('[HorribleSubs] Kakushigoto - 03 [720p].mkv', '1238837'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 03 [720p].mkv', '1238803'),
    #         ('[HorribleSubs] Gundam Build Divers Re-RISE - 15 [720p].mkv', '1238756'),
    #         ('[HorribleSubs] Infinite Dendrogram - 13 [720p].mkv', '1238628'),
    #         ('[HorribleSubs] number24 - 12 [720p].mkv', '1238616'),
    #         ('[HorribleSubs] Plunderer - 14 [720p].mkv', '1238564'),
    #         ('[HorribleSubs] Tower of God - 03 [720p].mkv', '1238524'),
    #         ('[HorribleSubs] Tamayomi - 03 [720p].mkv', '1238516'),
    #         ('[HorribleSubs] Ahiru no Sora - 27 [720p].mkv', '1238471'),
    #         ('[HorribleSubs] Houkago Teibou Nisshi - 02 [720p].mkv', '1238259'),
    #         ('[HorribleSubs] Black Clover - 130 [720p].mkv', '1238199'),
    #         ('[HorribleSubs] Shadowverse - 02 [720p].mkv', '1238189'),
    #         ('[HorribleSubs] Fruits Basket S2 (2019) - 02 [720p].mkv', '1238027'),
    #         ('[HorribleSubs] Princess Connect! Re Dive - 02 [720p].mkv', '1237995'),
    #         ('[HorribleSubs] Kitsutsuki Tanteidokoro - 01 [720p].mkv', '1237971'),
    #         ('[HorribleSubs] Shironeko Project - Zero Chronicle - 02 [720p].mkv', '1237958'),
    #         ('[HorribleSubs] Kingdom S3 - 02 [720p].mkv', '1237740'),
    #         ('[HorribleSubs] Gleipnir - 02 [720p].mkv', '1237668'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 02 [720p].mkv', '1237652'),
    #         ('[HorribleSubs] IDOLiSH7 S2 - 03 [720p].mkv', '1237632'),
    #         ('[HorribleSubs] Tsugumomo S2 - 02 [720p].mkv', '1237623'),
    #         ('[HorribleSubs] Boruto - Naruto Next Generations - 152 [720p].mkv', '1237527'),
    #         ('[HorribleSubs] Digimon Adventure (2020) - 02 [720p].mkv', '1237436'),
    #         ('[HorribleSubs] One Piece - 928 [720p].mkv', '1237427'),
    #         ('[HorribleSubs] Kaguya-sama wa Kokurasetai S2 - 01 [720p].mkv', '1237310'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 16 [720p].mkv', '1237305'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 02 [720p].mkv', '1237289'),
    #         ('[HorribleSubs] Hamefura - 02 [720p].mkv', '1237267'), ('[HorribleSubs] Arte - 02 [720p].mkv', '1237208'),
    #         ('[HorribleSubs] Major 2nd S2 - 02 [720p].mkv', '1237155'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 02 [720p].mkv', '1236973'),
    #         ('[HorribleSubs] Listeners - 02 [720p].mkv', '1236967'),
    #         ('[HorribleSubs] Bungo to Alchemist - Shinpan no Haguruma - 02 [720p].mkv', '1236943'),
    #         ('[HorribleSubs] Shokugeki no Soma S5 - 01 [720p].mkv', '1236919'),
    #         ('[HorribleSubs] Toaru Kagaku no Railgun T - 11 [720p].mkv', '1236906'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 02 [720p].mkv', '1236865'),
    #         ('[HorribleSubs] Appare-Ranman! - 01 [720p].mkv', '1236857'),
    #         ('[HorribleSubs] Zashiki Warashi no Tatami-chan - 01 [720p].mkv', '1236811'),
    #         ('[HorribleSubs] Fugou Keiji Balance - UNLIMITED - 01 [720p].mkv', '1236624'),
    #         ('[HorribleSubs] Gundam Build Divers Re-RISE - 14 [720p].mkv', '1236615'),
    #         ('[HorribleSubs] Kakushigoto - 02 [720p].mkv', '1236571'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 02 [720p].mkv', '1236546'),
    #         ('[HorribleSubs] Plunderer - 13 [720p].mkv', '1236348'),
    #         ('[HorribleSubs] BanG Dream! S3 - 13 [720p].mkv', '1236337'),
    #         ('[HorribleSubs] Tower of God - 02 [720p].mkv', '1236332'),
    #         ('[HorribleSubs] number24 - 11 [720p].mkv', '1236300'),
    #         ('[HorribleSubs] Tamayomi - 02 [720p].mkv', '1236280'),
    #         ('[HorribleSubs] Ahiru no Sora - 26 [720p].mkv', '1236232'),
    #         ('[HorribleSubs] Houkago Teibou Nisshi - 01 [720p].mkv', '1236021'),
    #         ('[HorribleSubs] Black Clover - 129 [720p].mkv', '1235974'),
    #         ('[HorribleSubs] Shadowverse - 01 [720p].mkv', '1235968'),
    #         ('[HorribleSubs] BanG Dream! S3 - 12 [720p].mkv', '1235964'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 11 [720p].mkv', '1235880'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 10 [720p].mkv', '1235875'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 09 [720p].mkv', '1235861'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 08 [720p].mkv', '1235849'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 07 [720p].mkv', '1235844'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 06 [720p].mkv', '1235840'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 05 [720p].mkv', '1235838'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 04 [720p].mkv', '1235831'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 03 [720p].mkv', '1235823'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 02 [720p].mkv', '1235820'),
    #         ('[HorribleSubs] Shironeko Project - Zero Chronicle - 01 [720p].mkv', '1235745'),
    #         ('[HorribleSubs] Fruits Basket S2 (2019) - 01 [720p].mkv', '1235732'),
    #         ('[HorribleSubs] Princess Connect! Re Dive - 01 [720p].mkv', '1235686'),
    #         ('[HorribleSubs] Jashin-chan Dropkick S2 - 01 [720p].mkv', '1235672'),
    #         ('[HorribleSubs] Kingdom S3 - 01 [720p].mkv', '1235451'),
    #         ('[HorribleSubs] Gleipnir - 01 [720p].mkv', '1235391'),
    #         ('[HorribleSubs] Shachou, Battle no Jikan desu! - 01 [720p].mkv', '1235370'),
    #         ('[HorribleSubs] IDOLiSH7 S2 - 02 [720p].mkv', '1235361'),
    #         ('[HorribleSubs] Tsugumomo S2 - 01 [720p].mkv', '1235349'),
    #         ('[HorribleSubs] Boruto - Naruto Next Generations - 151 [720p].mkv', '1235245'),
    #         ('[HorribleSubs] IDOLiSH7 S2 - 01 [720p].mkv', '1235226'),
    #         ('[HorribleSubs] Digimon Adventure (2020) - 01 [720p].mkv', '1235165'),
    #         ('[HorribleSubs] One Piece - 927 [720p].mkv', '1235156'),
    #         ('[HorribleSubs] Honzuki no Gekokujou - 15 [720p].mkv', '1235077'),
    #         ('[HorribleSubs] Yesterday wo Utatte - 01 [720p].mkv', '1235058'),
    #         ('[HorribleSubs] Hamefura - 01 [720p].mkv', '1235043'),
    #         ('[HorribleSubs] Gal to Kyouryuu - 01 [720p].mkv', '1235037'),
    #         ('[HorribleSubs] Arte - 01 [720p].mkv', '1234959'),
    #         ('[HorribleSubs] Major 2nd S2 - 01 [720p].mkv', '1234876'),
    #         ('[HorribleSubs] Boku no Hero Academia - 88 [720p].mkv', '1234829'),
    #         ('[HorribleSubs] Haikyuu!! S4 - 13 [720p].mkv', '1234746'),
    #         ('[HorribleSubs] Nami yo Kiitekure - 01 [720p].mkv', '1234721'),
    #         ('[HorribleSubs] Listeners - 01 [720p].mkv', '1234712'),
    #         ('[HorribleSubs] Bungo to Alchemist - Shinpan no Haguruma - 01 [720p].mkv', '1234700'),
    #         ('[HorribleSubs] Plunderer - 12 [720p].mkv', '1234691'),
    #         ('[HorribleSubs] Toaru Kagaku no Railgun T - 10 [720p].mkv', '1234664'),
    #         ('[HorribleSubs] Sakura Wars the Animation - 01 [720p].mkv', '1234642'),
    #         ('[HorribleSubs] Kakushigoto - 01 [720p].mkv', '1234453'),
    #         ('[HorribleSubs] Hachi-nan tte, Sore wa Nai deshou! - 01 [720p].mkv', '1234450'),
    #         ('[HorribleSubs] Infinite Dendrogram - 12 [720p].mkv', '1234427'),
    #         ("[HorribleSubs] Re Zero kara Hajimeru Isekai Seikatsu - Director's Cut - 13 [720p].mkv", '1234193'),
    #         ('[HorribleSubs] Tower of God - 01 [720p].mkv', '1234133'),
    #         ('[HorribleSubs] Tamayomi - 01 [720p].mkv', '1234126'),
    #         ('[HorribleSubs] Ahiru no Sora - 25 [720p].mkv', '1234075'),
    #         ('[HorribleSubs] Isekai Quartet S2 - 12 [720p].mkv', '1233914'),
    #         ('[HorribleSubs] Majutsushi Orphen Hagure Tabi - 13 [720p].mkv', '1233890'),
    #         ('[HorribleSubs] Black Clover - 128 [720p].mkv', '1233816'),
    #         ('[HorribleSubs] Ace of Diamond Act II - 52 [720p].mkv', '1233810'),
    #         ('[HorribleSubs] Granblue Fantasy The Animation S2 - 13 [720p].mkv', '1233749'),
    #         ('[HorribleSubs] ARP Backstage Pass - 10 [720p].mkv', '1233614'),
    #         ('[HorribleSubs] Phantasy Star Online 2 - Episode Oracle - 25 [720p].mkv', '1233603'),
    #         ('[HorribleSubs] Pet - 13 [720p].mkv', '1233574'),
    #         ('[HorribleSubs] Boruto - Naruto Next Generations - 150 [720p].mkv', '1233248'),
    #         ('[HorribleSubs] Gegege no Kitarou (2018) - 97 [720p].mkv', '1233193'),
    #         ('[HorribleSubs] PSYCHO-PASS 3 - First Inspector - 03 [720p].mkv', '1233177'),
    #         ('[HorribleSubs] PSYCHO-PASS 3 - First Inspector - 02 [720p].mkv', '1233173'),
    #         ('[HorribleSubs] One Piece - 926 [720p].mkv', '1233168'),
    #         ('[HorribleSubs] PSYCHO-PASS 3 - First Inspector - 01 [720p].mkv', '1233166'),
    #         ('[HorribleSubs] Kyokou Suiri - 12 [720p].mkv', '1233075'),
    #         ('[HorribleSubs] Magia Record - 13 [720p].mkv', '1233041'),
    #         ('[HorribleSubs] Ishuzoku Reviewers - 12 [720p].mkv', '1233022'),
    #         ('[HorribleSubs] Nanabun no Nijyuuni - 12 [720p].mkv', '1233021'),
    #         ('[HorribleSubs] Boku no Tonari ni Ankoku Hakaishin ga Imasu - 12 [720p].mkv', '1232956'),
    #         ('[HorribleSubs] Cardfight!! Vanguard - Zoku Koukousei-hen - 45 [720p].mkv', '1232949'),
    #         ('[HorribleSubs] Detective Conan - 974 [720p].mkv', '1232910'),
    #         ('[HorribleSubs] Boku no Hero Academia - 87 [720p].mkv', '1232879'),
    #         ('[HorribleSubs] Runway de Waratte - 12 [720p].mkv', '1232766'),
    #         ('[HorribleSubs] Haikyuu!! S4 - 12 [720p].mkv', '1232753'),
    #         ('[HorribleSubs] Oda Cinnamon Nobunaga - 12 [720p].mkv', '1232734'),
    #         ('[HorribleSubs] Kabukicho Sherlock - 24 [720p].mkv', '1232730'),
    #         ('[HorribleSubs] Toaru Kagaku no Railgun T - 09 [720p].mkv', '1232682'),
    #         ('[HorribleSubs] Koisuru Asteroid - 12 [720p].mkv', '1232649'),
    #         ('[HorribleSubs] Jibaku Shounen Hanako-kun - 12 [720p].mkv', '1232469'),
    #         ('[HorribleSubs] Oshi ga Budoukan Ittekuretara Shinu - 12 [720p].mkv', '1232421'),
    #         ('[HorribleSubs] Housekishou Richard-shi no Nazo Kantei - 12 [720p].mkv', '1232399'),
    #         ('[HorribleSubs] Somali to Mori no Kamisama - 12 [720p].mkv', '1232375'),
    #         ('[HorribleSubs] Infinite Dendrogram - 11 [720p].mkv', '1232355'),
    #         ('[HorribleSubs] Hatena Illusion - 11 [720p].mkv', '1232342'),
    #         ('[HorribleSubs] Show By Rock!! Mashumairesh!! - 12 [720p].mkv', '1232341'),
    #         ('[HorribleSubs] Nekopara - 12 [720p].mkv', '1232317'),
    #         ('[HorribleSubs] Mugen no Juunin - Immortal - 24 [720p].mkv', '1232132'),
    #         ("[HorribleSubs] Re Zero kara Hajimeru Isekai Seikatsu - Director's Cut - 12 [720p].mkv", '1232095'), (
    #             '[HorribleSubs] Itai no wa Iya nano de Bougyoryoku ni Kyokufuri Shitai to Omoimasu - 12 [720p].mkv',
    #             '1232091'), ('[HorribleSubs] Kono Subarashii Sekai ni Shukufuku wo! Movie - 00 [720p].mkv', '1232000'),
    #         ('[HorribleSubs] Chihayafuru S3 - 24 [720p].mkv', '1231885'),
    #         ('[HorribleSubs] Isekai Quartet S2 - 11 [720p].mkv', '1231824'),
    #         ('[HorribleSubs] Majutsushi Orphen Hagure Tabi - 12 [720p].mkv', '1231805'),
    #         ('[HorribleSubs] Black Clover - 127 [720p].mkv', '1231763'),
    #         ('[HorribleSubs] Ace of Diamond Act II - 51 [720p].mkv', '1231740'),
    #         ('[HorribleSubs] Murenase! Seton Gakuen - 12 [720p].mkv', '1231542'),
    #         ('[HorribleSubs] Yatogame-chan Kansatsu Nikki S2 - 12 [720p].mkv', '1231536'),
    #         ('[HorribleSubs] ARP Backstage Pass - 09 [720p].mkv', '1231523'),
    #         ('[HorribleSubs] Phantasy Star Online 2 - Episode Oracle - 24 [720p].mkv', '1231504'),
    #         ('[HorribleSubs] Heya Camp - 12 [720p].mkv', '1231469'), ('[HorribleSubs] Pet - 12 [720p].mkv', '1231466')]


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
            temp = re.findall("\[HorribleSubs\] (.+?) - ([0-9]+?) \[720p\].mkv", row[0])
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
        qb = Client('http://127.0.0.1:8080/')
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
    while True:
        choice = input("""\nKon'nichiwa! Hajimemashite!
What do you want to do?
1. Add new anime
2. Update progress on existing anime
3. View progress on existing anime
4. All currently watching anime
5. Check for new episodes.
6. Exit
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
                                add_torrent(f"{row[-1]}.torrent")
                                print("Added to torrent!\n")
                                os.remove(f"{row[-1]}.torrent")

                        else:
                            print("\nOkay!")
                else:
                    print("The anime is not being aired this season.")
            else:
                print("\nAnime does not exist")
        elif choice == "6":
            break
        else:
            print("Invalid input\n")


if __name__ == '__main__':
    main()
