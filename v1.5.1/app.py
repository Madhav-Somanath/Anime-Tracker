from utils_anime import add_anime, update_anime, view_anime_progress, delete_anime
from utils_scrape import check_new_episodes, scrape_data


def main():
    scrape_flag = False

    view_anime_progress()
    while True:
        choice = input("""Kon'nichiwa! Hajimemashite!
What do you want to do?
1. Add new anime
2. Update progress on existing anime
3. All currently watching anime
4. Check for new episodes of all currently watching anime
5. Delete Anime
6. Exit
Enter your choice:> """)

        if choice == '1':
            anime_name = input("Enter the name of the anime: ")
            current_episode = int(input("Enter the current episode number: "))
            total_episodes = int(input("Enter the total number of episodes: "))
            add_anime(anime_name, current_episode, total_episodes)
        elif choice == '2':
            update_anime()
        elif choice == '3':
            view_anime_progress()
        elif choice == '4':
            if not scrape_flag:
                all_anime = scrape_data()
                scrape_flag = True
            check_new_episodes(all_anime)
        elif choice == '5':
            delete_anime()
        elif choice == '6':
            print("Sayonara!")
            break

        else:
            print("Invalid character")


if __name__ == '__main__':
    main()
