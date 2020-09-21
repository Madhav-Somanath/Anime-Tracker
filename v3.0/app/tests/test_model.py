from django.test import TestCase
from app.utils.database_script import *


# models test
class ModelTest(TestCase):

    def test_model_data_1(self):
        """To check normal data values"""
        name = "Kakushigoto"
        current_episode = 2
        total_episodes = 20
        AnimeModel.objects.create(name=name,
                                  current_episode=current_episode,
                                  total_episodes=total_episodes)

        data = AnimeModel.objects.get(name=name)
        self.assertEqual(name, data.name)
        self.assertEqual(current_episode, data.current_episode)
        self.assertEqual(total_episodes, data.total_episodes)

    def test_model_data_2(self):
        """To check with current_episode=0"""
        name = "Kakushigoto"
        total_episodes = 20
        AnimeModel.objects.create(name=name,
                                  total_episodes=total_episodes)

        data = AnimeModel.objects.get(name=name)
        self.assertEqual(name, data.name)
        self.assertEqual(0, data.current_episode)
        self.assertEqual(total_episodes, data.total_episodes)

    def test_model_data_3(self):
        """To test add_anime_to_database function"""
        name = "Attack on titan"
        current_episode = 2
        total_episodes = 20

        flag = add_anime_to_database(name, current_episode, total_episodes)

        data = AnimeModel.objects.get(name=name)

        self.assertTrue(flag)
        self.assertEqual(name, data.name)
        self.assertEqual(current_episode, data.current_episode)
        self.assertEqual(total_episodes, data.total_episodes)

    def test_model_data_4(self):
        """To test get_anime_to_database function for one entry"""
        name = "Attack on titan"
        current_episode = 2
        total_episodes = 20

        AnimeModel.objects.create(name=name,
                                  current_episode=current_episode,
                                  total_episodes=total_episodes)

        data = get_all_anime_from_database()
        anime_id = AnimeModel.objects.get(name=name).id
        expected = [(anime_id, name, current_episode, total_episodes)]

        self.assertEqual(data, expected)

    def test_model_data_5(self):
        """To test get_anime_from_database function for more than one entry"""
        name1 = "Attack on Titan"
        current_episode1 = 2
        total_episodes1 = 20

        name2 = "Kakushigoto"
        current_episode2 = 1
        total_episodes2 = 15

        AnimeModel.objects.create(name=name1,
                                  current_episode=current_episode1,
                                  total_episodes=total_episodes1)
        AnimeModel.objects.create(name=name2,
                                  current_episode=current_episode2,
                                  total_episodes=total_episodes2)

        data = get_all_anime_from_database()
        anime_id1 = AnimeModel.objects.get(name=name1).id
        anime_id2 = AnimeModel.objects.get(name=name2).id

        expected = [(anime_id1, name1, current_episode1, total_episodes1),
                    (anime_id2, name2, current_episode2, total_episodes2)]

        self.assertEqual(data, expected)

    def test_model_data_6(self):
        """To test update_anime_in_database function without total_episodes argument"""
        name = "Attack on Titan"
        current_episode = 2
        total_episodes = 20

        AnimeModel.objects.create(name=name,
                                  current_episode=current_episode,
                                  total_episodes=total_episodes)
        anime_id = AnimeModel.objects.get(name=name).id

        current_episode = 5
        flag = update_anime_in_database(anime_id, current_episode)

        current_episode_in_database = AnimeModel.objects.get(id=anime_id).current_episode

        self.assertTrue(flag)
        self.assertEqual(current_episode, current_episode_in_database)

    def test_model_data_7(self):
        """To test update_anime_in_database function with total_episodes argument"""
        name = "Your name 1"
        current_episode = 1
        total_episodes = 30

        AnimeModel.objects.create(name=name,
                                  current_episode=current_episode,
                                  total_episodes=total_episodes)
        anime_id = AnimeModel.objects.get(name=name).id

        current_episode = 7
        total_episodes = 35
        update_anime_in_database(anime_id, current_episode, total_episodes)

        current_episode_in_database = AnimeModel.objects.get(id=anime_id).current_episode
        total_episodes_in_database = AnimeModel.objects.get(id=anime_id).total_episodes

        self.assertEqual(current_episode, current_episode_in_database)
        self.assertEqual(total_episodes, total_episodes_in_database)

    def test_model_data_8(self):
        """To test delete_anime_from_database function"""
        name = "Your name 2"
        current_episode = 1
        total_episodes = 30

        AnimeModel.objects.create(name=name,
                                  current_episode=current_episode,
                                  total_episodes=total_episodes)
        anime_id = AnimeModel.objects.get(name=name).id

        delete_anime_from_database(anime_id)

        self.assertFalse(AnimeModel.objects.filter(id=anime_id))

    def test_model_data_9(self):
        """To test get_one_anime function"""
        name = "Bleach"
        current_episode = 3
        total_episodes = 10

        AnimeModel.objects.create(name=name,
                                  current_episode=current_episode,
                                  total_episodes=total_episodes)
        anime_id = AnimeModel.objects.get(name=name).id

        data = get_one_anime(anime_id)
        expected = [(anime_id, name, current_episode, total_episodes)]

        self.assertEqual(data, expected)

    def test_model_data_10(self):
        """To test get_anime_from_database function for empty database"""
        data = get_all_anime_from_database()

        self.assertEqual(data, [])
