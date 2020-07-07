from utils_anime import add_anime, update_anime, view_anime_progress
from utils_scrape import check_new_episodes, scrape_data


def main():
    scrape_flag = False

    while True:
        choice = input("""Kon'nichiwa! Hajimemashite!
What do you want to do?
1. Add new anime
2. Update progress on existing anime
3. All currently watching anime
4. Check for new episodes of all currently watching anime.
5. Exit
Enter your choice:> """)

        if choice == '1':
            add_anime()
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
            print("Sayonara!")
            break

        else:
            print("Invalid character")


if __name__ == '__main__':
    main()
