import os
import forms
from app import app
from flask import render_template, request
from utils_database import add_anime_to_database, get_all_anime_from_database, update_anime_in_database, delete_anime_from_database
from utils_scrape import scrape_data, check_new_episodes
from utils_torrent import download_torrent, add_torrent


ANIME_DOWNLOAD_PATH = "D:\Anime"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add-anime', methods=("GET", "POST"))
def add_anime_page():
    form = forms.AddAnimeForm()
    if form.validate_on_submit():
        anime_name = request.form.get("anime_name")
        current_episode = int(request.form.get("current_episode"))
        total_episodes = int(request.form.get("total_episodes"))
        # TODO: Add form validation.

        if add_anime_to_database(anime_name, current_episode, total_episodes):
            return render_template("add_anime.html", form=form, anime_name=form.anime_name.data)
        else:
            pass
            # TODO: Show error message.

    return render_template("add_anime.html", form=form)


@app.route('/update-anime', methods=("GET", "POST"))
def update_anime_page():
    form = forms.AddAnimeForm()
    all_anime = get_all_anime_from_database()

    if request.method == "POST":
        anime_id = int(request.form["anime-id"])
        current_episode = int(request.form.get(f"current-episode-{anime_id}"))  # As we have to get the data from the input field of that particular anime.
        total_episodes = int(request.form.get(f"total-episodes-{anime_id}"))

        if update_anime_in_database(anime_id, current_episode, total_episodes):
            return render_template("update_anime.html", form=form, all_anime=all_anime, success=True)

    return render_template("update_anime.html", form=form, all_anime=all_anime)


@app.route('/all-anime')
def all_anime_page():
    all_anime = get_all_anime_from_database()

    return render_template("all_anime.html", all_anime=all_anime)


@app.route('/check-anime', methods=("GET", "POST"))
def check_new_anime():
    if request.method == 'POST':
        horriblesubs_data = scrape_data()

        new_episodes, anime_id_mapping = check_new_episodes(horriblesubs_data)
        if request.form.get("check_anime_button", None) == "Click here to check":
            return render_template("check_anime.html", data=new_episodes)

        elif request.form.get("download-button", None):
            anime_name = request.form.get("download-button")
            already_downloaded_anime = os.listdir(ANIME_DOWNLOAD_PATH)
            latest_episode_number = 0

            for row in new_episodes[anime_name]:                # row format: ('<anime name>', 7, '1271478')
                if f"[HorribleSubs] {row[0]} - {row[1] if row[1] > 10 else '0' + str(row[1])} [720p].mkv" not in already_downloaded_anime:
                    download_torrent(f"https://nyaa.si/download/{row[-1]}.torrent")
                    if add_torrent(f"{row[-1]}.torrent"):
                        latest_episode_number = max(latest_episode_number, row[1])
                    else:
                        print("Couldn't add torrent!")
                    os.remove(f"{row[-1]}.torrent")

            update_anime_in_database(anime_id_mapping[anime_name], latest_episode_number)
            del new_episodes[anime_name]

            return render_template("check_anime.html", data=new_episodes)
    return render_template("check_anime.html")


@app.route('/delete-anime', methods=("GET", "POST"))
def delete_anime():
    form = forms.AddAnimeForm()
    all_anime = get_all_anime_from_database()

    if request.method == "POST":
        anime_id = int(request.form['anime-id'])

        if delete_anime_from_database(anime_id):
            all_anime = get_all_anime_from_database()
            return render_template("delete_anime.html", form=form, all_anime=all_anime, success=True)

    return render_template("delete_anime.html", form=form, all_anime=all_anime)


