from flask import Flask, render_template, url_for, redirect, request, flash
from app import app
from utils_database import *


@app.route('/')
def index():
    all_anime = get_all_anime_from_database()

    return render_template("index.html", all_anime=all_anime)


@app.route('/add-anime', methods=["GET", "POST"])
def add_anime():
    if request.method == "POST":
        anime_name = request.form.get("anime-name")
        current_episode = request.form.get("current-episode").strip()
        total_episodes = request.form.get("total-episodes").strip()

        current_episode_check = "is-invalid" if not current_episode.isnumeric() else "is-valid"
        total_episode_check = "is-invalid" if not total_episodes.isnumeric() else "is-valid"

        if current_episode_check == "is-invalid" or total_episode_check == "is-invalid":
            flash("Must be a number!")

            context = {
                "anime_name": anime_name,
                "current_episode": current_episode,
                "total_episodes": total_episodes,
                "current_episode_check": current_episode_check,
                "anime_name_check": "is-valid",
                "total_episode_check": total_episode_check,
                "alert_color": "danger"
            }
            return render_template("add.html", **context)
        else:
            current_episode = int(current_episode)
            total_episodes = int(total_episodes)

            if add_anime_to_database(anime_name, current_episode, total_episodes):
                flash("Anime successfully added to database!")

                return render_template("add.html", alert_color="success")

    return render_template("add.html")


@app.route('/update-anime/<int:anime_id>', methods=["GET", "POST"])
def update_anime(anime_id):
    data = get_one_anime(anime_id)[0]

    context = {
        "anime_id": anime_id,
        "anime_name": data[1],
        "current_episode": data[2],
        "total_episodes": data[3],
        "flag": True
    }

    if request.method == "POST":
        anime_name = request.form.get("anime-name")
        current_episode = request.form.get("current-episode").strip()
        total_episodes = request.form.get("total-episodes").strip()

        current_episode_check = "is-invalid" if not current_episode.isnumeric() else "is-valid"
        total_episode_check = "is-invalid" if not total_episodes.isnumeric() else "is-valid"

        if current_episode_check == "is-invalid" or total_episode_check == "is-invalid":
            flash("Must be a number!")

            context = {
                "anime_name": anime_name,
                "current_episode": current_episode,
                "total_episodes": total_episodes,
                "current_episode_check": current_episode_check,
                "anime_name_check": "is-valid",
                "total_episode_check": total_episode_check,
                "alert_color": "danger",
                "flag": True
            }
            return render_template("add.html", **context)
        else:
            update_anime_in_database(anime_id, current_episode, total_episodes)
            flash("Anime successfully updated!")

            return render_template("update.html", flag=False)

    return render_template("update.html", **context)


@app.route('/delete-anime/<int:anime_id>', methods=["GET", "POST"])
def delete_anime(anime_id):
    flag = True
    anime_name = get_one_anime(anime_id)[0][1]     # Format: [(6, 'Enen no Shouboutai S2', 5, 24)]
    if request.form.get("delete_button") == "Submit":
        if delete_anime_from_database(anime_id):
            flash("Anime Successfully deleted")
            flag = False
        else:
            print("error")
    return render_template("delete.html", anime_name=anime_name, anime_id=anime_id, flag=flag)


