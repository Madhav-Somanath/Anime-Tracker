# Relative path to the database text file
DATABASE_PATH = "resources/anime.txt"


def add_anime(anime_name, episodes, current_episode_=0):
    """
    Function to add a new anime to the database /resources/anime.txt

    Args:
        anime_name (str): Name of the anime.
        episodes (int): Total episodes in the anime.
        current_episode_ (int) : Current episode count
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
    Doctest:
        >>> anime_exists("Tower of God")
        True
        >>> anime_exists("Apple")
        False
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
    anime_data = []
    with open(DATABASE_PATH, "r") as file:
        anime_data = file.readlines()

    # for idx, anime_ in enumerate(anime_data):
    #     print(f"{idx + 1}. {anime_[0]} {anime_[]}/{anime_[2]}")
    for idx, anime_ in enumerate(anime_data):
        line_list = anime_.split("~")
        if anime_name in line_list[0]:
            anime_data[idx] = f"{line_list[0]}~{episode}~{line_list[2]}"
            break

    anime_data.sort()
    with open(DATABASE_PATH, "w") as file:
        file.writelines(anime_data)

    print(f"\nSuccess! Updated the episode count!\n\n")


def anime_progress(anime_name):
    """
    Function to list the current progress of the anime.
    We read the data from the database.

    Args:
          anime_name (str): Name of the anime.
    Returns:
        (tuple): (Current episode, Total episodes)
    Doctest:
        >>> anime_progress("Tower of God")
        ('0', '12')
        >>> anime_progress("Gintama")
        ('3', '12')
    """

    with open(DATABASE_PATH, "r") as file:
        for line in file:
            line_list = line.split("~")
            if anime_name in line_list[0]:
                return tuple([line_list[1], line_list[2].rstrip("\n")])


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
        choice = input("""Kon'nichiwa(こんにちは)! Hajimemashite(はじめまして)!
What do you want to do?
1. Add new anime
2. Update progress on existing anime
3. View progress on existing anime
4. All currently watching anime
5. Exit
Enter your choice:> """)

        if choice == "1":
            new_anime = input("Enter the name of the anime:> ")
            current_episode = int(input("Enter the current episode number:> "))
            total_episodes = int(input("Enter the total number of episodes:> "))

            if not anime_exists(new_anime):
                add_anime(new_anime, total_episodes, current_episode)
            else:
                print("Anime already exists")
        elif choice == "2":
            anime_input = input("Enter the name of the anime:> ")
            if anime_exists(anime_input):
                current_episode = int(input("Enter the current episode number:> "))
                update_anime(anime_input, current_episode)
            else:
                print("\nThe anime does not exist.\n")
        elif choice == "3":
            anime_input = input("Enter the name of the anime:> ")
            if anime_exists(anime_input):
                current, total = anime_progress(anime_input)
                print(f"{anime_input}: {current}/{total}\n")
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
    # import doctest
    # doctest.testmod()
    print("Current Watch list:\n")
    all_anime = anime_progress_all()
    if all_anime == ():
        print("You are watching no anime currently\n")
    else:
        for anime in all_anime:
            print(f"{anime[0]}: {anime[1]}/{anime[2]}\n", end="")
        print()

    main()
