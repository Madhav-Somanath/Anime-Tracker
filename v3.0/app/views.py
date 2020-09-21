from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from app.utils.database_script import *
import time
from celery import task
from celery import shared_task
from celery_progress.backend import ProgressRecorder


class AddAnimeView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        return render(request, "app/add.html")

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        anime_name = request.POST["anime-name"]
        current_episode = request.POST["current-episode"].strip()
        total_episodes = request.POST["total-episodes"].strip()
        message = ""

        current_episode_check = "is-invalid" if not current_episode.isnumeric() else "is-valid"
        total_episode_check = "is-invalid" if not total_episodes.isnumeric() else "is-valid"

        if current_episode_check == "is-invalid" or total_episode_check == "is-invalid":
            message = "Must be a number!"
            context = {
                "anime_name": anime_name,
                "current_episode": current_episode,
                "total_episodes": total_episodes,
                "current_episode_check": current_episode_check,
                "anime_name_check": "is-valid",
                "total_episode_check": total_episode_check,
                "alert_color": "danger",
                "message": message
            }

            return render(request, "app/add.html", context=context)

        else:
            current_episode = int(current_episode)
            total_episodes = int(total_episodes)

            flag = add_anime_to_database(anime_name, current_episode, total_episodes)
            if flag:
                message = "Anime successfully added to database!"
            return render(request, "app/add.html", context={"alert_color": "success",
                                                            "message": message})


class UpdateAnimeView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, anime_id):
        data = get_one_anime(anime_id)[0]

        context = {
            "anime_id": anime_id,
            "anime_name": data[1],
            "current_episode": data[2],
            "total_episodes": data[3],
            "flag": True
        }

        return render(request, "app/update.html", context=context)

    # noinspection PyMethodMayBeStatic
    def post(self, request, anime_id):
        anime_name = get_one_anime(anime_id)[0][1]
        current_episode = request.POST.get("current-episode").strip()
        total_episodes = request.POST.get("total-episodes").strip()

        current_episode_check = "is-invalid" if not current_episode.isnumeric() else "is-valid"
        total_episode_check = "is-invalid" if not total_episodes.isnumeric() else "is-valid"

        if current_episode_check == "is-invalid" or total_episode_check == "is-invalid":
            message = "Must be a number!"

            context = {
                "anime_name": anime_name,
                "current_episode": current_episode,
                "total_episodes": total_episodes,
                "current_episode_check": current_episode_check,
                "anime_name_check": "is-valid",
                "total_episode_check": total_episode_check,
                "alert_color": "danger",
                "flag": True,
                "message": message
            }
            return render(request, "app/update.html", context=context)
        else:
            update_anime_in_database(anime_id, current_episode, total_episodes)
            message = "Anime successfully updated!"

            context = {
                "message": message,
                "flag": False
            }

            return render(request, "app/update.html", context=context)


class IndexView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        all_anime = get_all_anime_from_database()
        return render(request, "app/index.html", context={"all_anime": all_anime})


class DeleteAnimeView(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, anime_id):
        anime_name = get_one_anime(anime_id)[0][1]  # Format: [(6, 'Enen no Shouboutai S2', 5, 24)]

        context = {"anime_name": anime_name,
                   "flag": True}

        return render(request, "app/delete.html", context=context)

    # noinspection PyMethodMayBeStatic
    def post(self, request, anime_id):
        context = None
        if delete_anime_from_database(anime_id):
            context = {"message": "Anime Successfully deleted",
                       "flag": False}

        return render(request, "app/delete.html", context=context)


@task
def my_task():
    for i in range(100):
        pass
    print("done")



class DownloadAnimeView(View):

    def get(self, request):

        return HttpResponseRedirect("http://127.0.0.1:8000/download")

    def post(self):
        pass
