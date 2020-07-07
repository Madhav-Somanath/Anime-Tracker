from utils_anime import add_anime, update_anime, view_anime_progress


def main():
    while True:
        choice = input("""Kon'nichiwa! Hajimemashite!
What do you want to do?
1. Add new anime
2. Update progress on existing anime
3. All currently watching anime
4. Check for new episodes of a particular anime.
5. Check for new episodes of all currently watching anime.
6. Exit
Enter your choice:> """)

        if choice == '1':
            add_anime()
        elif choice == '2':
            update_anime()
        elif choice == '3':
            view_anime_progress()
        elif choice == '4':
            pass
        elif choice == '5':
            pass
        elif choice == '6':
            print("Sayonara!")
            break

        else:
            print("Invalid character")


if __name__ == '__main__':
    main()
