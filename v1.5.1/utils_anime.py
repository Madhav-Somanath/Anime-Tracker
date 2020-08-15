import sqlite3

DATABASE_NAME = "anime_database"
TABLE_NAME = "anime"


def add_anime(anime_name, current_episode, total_episodes) -> None:
    """
    Function to add anime to database.
    :return: None
    """
    with sqlite3.connect(f'{DATABASE_NAME}.s3db') as conn:
        cur = conn.cursor()
        query = "INSERT INTO " \
                f"   {TABLE_NAME}(name, current_episode, total_episodes)" \
                "VALUES " \
                f"   ('{anime_name}', '{current_episode}', '{total_episodes}')" \
                ";"
        cur.execute(query)
        conn.commit()

    print(f"\nSuccess!\nAdded {anime_name} to database.\n")


def get_all_anime() -> list:
    """
    Function to get all the anime in the database.
    :return anime_in_database:
        tuple of tuples: Tuple of Tuples in the format ((id, anime-name, current-episode, total-episodes))
    """

    with sqlite3.connect(f'{DATABASE_NAME}.s3db') as conn:
        cur = conn.cursor()
        query = f"SELECT * FROM {TABLE_NAME};"
        cur.execute(query)
        anime_in_database = cur.fetchall()
    return anime_in_database


def view(anime_in_database) -> None:
    """
    Function to display all the anime in the database.
    :param anime_in_database: list
    :return: None
    """
    print("\nCurrent Anime Watchlist:")
    for idx, anime in enumerate(anime_in_database):
        print(f"{idx + 1}. {anime[1]}: {anime[2]}/{anime[3]}")
    print()


def view_anime_progress():
    """
    Driver function to view data.
    :return: None
    """
    anime_in_database = get_all_anime()
    view(anime_in_database)


def update_anime(anime_id=None, current_episode=None):
    """
    Function to update anime in database.
    :return: None
    """
    if anime_id is None:
        anime_in_database = get_all_anime()
        view(anime_in_database)
        choice = int(input("Enter the id from the list above: "))
    if anime_id is None and choice > len(anime_in_database):
        print("Invalid choice\n")
    else:
        if anime_id is None:
            anime_id = anime_in_database[choice - 1][0]
            current_episode = int(input("Enter the current episode: "))
        with sqlite3.connect(f'{DATABASE_NAME}.s3db') as conn:
            cur = conn.cursor()
            query = "UPDATE" \
                    f"  {TABLE_NAME} " \
                    "SET" \
                    f"  current_episode = {current_episode} " \
                    "WHERE" \
                    f"  id = {anime_id}" \
                    ";"
            cur.execute(query)
            conn.commit()
            print("Episode count updated!\n")


def delete_anime(anime_id=None, current_episode=None):
    if anime_id is None:
        anime_in_database = get_all_anime()
        view(anime_in_database)
        choice = int(input("Enter the id from the list above: "))
    if anime_id is None and choice > len(anime_in_database):
        print("Invalid choice\n")
    else:
        if anime_id is None:
            anime_id = anime_in_database[choice - 1][0]
        with sqlite3.connect(f'{DATABASE_NAME}.s3db') as conn:
            cur = conn.cursor()
            query = "DELETE FROM " \
                    f"{TABLE_NAME} " \
                    f"WHERE" \
                    f" id = {anime_id};"
            cur.execute(query)
            conn.commit()
            print(f"Anime deleted from database!\n")

# Table schema
#         "CREATE TABLE anime("  \
#         "id INTEGER PRIMARY KEY AUTOINCREMENT," \
#         "name VARCHAR(50)," \
#         "current_episode INTEGER NOT NULL DEFAULT 0," \
#         "total_episodes INTEGER NOT NULL);"
