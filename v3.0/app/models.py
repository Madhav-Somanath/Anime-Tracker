from django.db import models


class AnimeModel(models.Model):
    name = models.CharField(max_length=100)
    current_episode = models.IntegerField(default=0)
    total_episodes = models.IntegerField()
