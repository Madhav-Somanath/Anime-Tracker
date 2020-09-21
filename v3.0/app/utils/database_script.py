from app.models import AnimeModel


def add_anime_to_database(anime_name: str, current_episode: int, total_episodes: int) -> bool:
    """
    Function to add anime to an sqlite3 database.
    :param anime_name: Name of the anime.
    :param current_episode: Current episode number.
    :param total_episodes: Total number of episodes.
    :return: bool
    """
    anime = AnimeModel.objects.create(name=anime_name,
                                      current_episode=current_episode,
                                      total_episodes=total_episodes)
    return True


def get_all_anime_from_database() -> list:
    """
    Function to get all the anime in the database.
    :return anime_in_database:
        list of tuples: Tuple of Tuples in the format ((id, anime-name, current-episode, total-episodes))
    """
    all_objects = AnimeModel.objects.all()

    anime_in_database = []
    for anime in all_objects:
        anime_in_database.append((anime.id, anime.name, anime.current_episode, anime.total_episodes))

    return sorted(anime_in_database, key=lambda x: x[1])


def update_anime_in_database(anime_id: int, current_episode: int, total_episodes=None) -> bool:
    """
    Function to update anime in the database.
    :param anime_id: Id of the anime in database.
    :param current_episode: Current episode number.
    :param total_episodes: Total number of episode.
    :return: True if no problems else False.
    """
    anime_object = AnimeModel.objects.filter(id=anime_id)
    anime_object.update(current_episode=current_episode)
    if total_episodes:
        anime_object.update(total_episodes=total_episodes)

    return True


def delete_anime_from_database(anime_id: int) -> bool:
    """
    Function to delete anime from database.
    :param anime_id: Id of anime in database.
    :return: True if no errors else False.
    """
    AnimeModel.objects.filter(id=anime_id).delete()

    return True


def get_one_anime(anime_id: int) -> list:
    """
    Function that returns the details of a particular anime.
    :param anime_id:  Id of the anime in the database.
    :return:    List in the form: [(6, 'Enen no Shouboutai S2', 5, 24)]
    """
    model = AnimeModel.objects.get(id=anime_id)

    return [(anime_id, model.name, model.current_episode, model.total_episodes)]
