import sqlite3

# Path to old database
DATABASE_NAME = "database\\test_database.s3db"
TABLE_NAME = "anime"


def add_anime_to_database(anime_name: str, current_episode: int, total_episodes: int) -> bool:
    """
    Function to add anime to an sqlite3 database.
    :param anime_name: Name of the anime.
    :param current_episode: Current episode number.
    :param total_episodes: Total number of episodes.
    :return: bool
    """
    with sqlite3.connect(f'{DATABASE_NAME}') as conn:
        cur = conn.cursor()
        query = "INSERT INTO " \
                f"   {TABLE_NAME}(name, current_episode, total_episodes)" \
                "VALUES " \
                f"   ('{anime_name}', '{current_episode}', '{total_episodes}')" \
                ";"
        cur.execute(query)
        conn.commit()

    return True


def get_all_anime_from_database() -> list:
    """
    Function to get all the anime in the database.
    :return anime_in_database:
        tuple of tuples: Tuple of Tuples in the format ((id, anime-name, current-episode, total-episodes))
    """

    with sqlite3.connect(f'{DATABASE_NAME}') as conn:
        cur = conn.cursor()
        query = f"SELECT * FROM {TABLE_NAME};"
        cur.execute(query)
        anime_in_database = cur.fetchall()
    return sorted(anime_in_database, key=lambda x: x[1])


def update_anime_in_database(anime_id: int, current_episode: int, total_episodes=None) -> bool:
    """
    Function to update anime in the database.
    :param anime_id: Id of the anime in database.
    :param current_episode: Current episode number.
    :param total_episodes: Total number of episode.
    :return: True if no problems else False.
    """
    try:
        with sqlite3.connect(f'{DATABASE_NAME}') as conn:
            cur = conn.cursor()
            print(total_episodes)
            if not total_episodes:
                print("correct query")
                query = "UPDATE" \
                        f"  {TABLE_NAME} " \
                        "SET" \
                        f"  current_episode = {current_episode} " \
                        "WHERE" \
                        f"  id = {anime_id}" \
                        ";"
            else:
                query = "UPDATE" \
                        f"  {TABLE_NAME} " \
                        "SET" \
                        f"  current_episode = {current_episode}, " \
                        f"  total_episodes =  {total_episodes} " \
                        "WHERE" \
                        f"  id = {anime_id}" \
                        ";"
            cur.execute(query)
            conn.commit()
    except:
        return False

    return True


def delete_anime_from_database(anime_id: int) -> bool:
    """
    Function to delete anime from database.
    :param anime_id: Id of anime in database.
    :return: True if no errors else False.
    """
    try:
        with sqlite3.connect(f'{DATABASE_NAME}') as conn:
            cur = conn.cursor()
            query = "DELETE FROM " \
                    f"{TABLE_NAME} " \
                    f"WHERE" \
                    f" id = {anime_id};"
            cur.execute(query)
            conn.commit()
    except:
        return False

    return True


def get_one_anime(anime_id: int):
    """
    Function that returns the details of a particular anime.
    :param anime_id:  Id of the anime in the database.
    :return:    List in the form: [(6, 'Enen no Shouboutai S2', 5, 24)]
    """
    with sqlite3.connect(f'{DATABASE_NAME}') as conn:
        cur = conn.cursor()
        query = f"SELECT * FROM {TABLE_NAME} " \
                f"WHERE id = {anime_id} " \
                f";"
        cur.execute(query)
        anime_in_database = cur.fetchall()
    return anime_in_database



# Database schema
# if __name__ == '__main__':
#     with sqlite3.connect(f'{DATABASE_NAME}') as conn:
#         cur = conn.cursor()
#         query = "CREATE TABLE anime("  \
#             "id INTEGER PRIMARY KEY AUTOINCREMENT," \
#             "name VARCHAR(50)," \
#             "current_episode INTEGER NOT NULL DEFAULT 0," \
#             "total_episodes INTEGER NOT NULL);"
#         cur.execute(query)
#         conn.commit()
#     with sqlite3.connect(f'{DATABASE_NAME}') as conn:
#         cur = conn.cursor()
#         query = "UPDATE" \
#                 f"  {TABLE_NAME} " \
#                 "SET" \
#                 f"  current_episode = 1, " \
#                 f"  total_episodes =  2 " \
#                 "WHERE" \
#                 f"  id = {1}" \
#                 ";"
#         cur.execute(query)
#         conn.commit()
