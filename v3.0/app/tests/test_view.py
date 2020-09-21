from django.test import TestCase
import requests
from selenium import webdriver
from app.models import AnimeModel
import time


# views test
class ModelTest(TestCase):
    def test_view_1(self):
        """To test if the index page is displayed"""
        url = "http://127.0.0.1:8000"
        r = requests.get(url)

        self.assertEqual(r.status_code, 200)

    def test_view_2(self):
        """To test if the add page is displayed"""
        url = "http://127.0.0.1:8000/add"
        r = requests.get(url)

        self.assertEqual(r.status_code, 200)

    def test_view_3(self):
        """To test if the add page is displayed"""
        url = "http://127.0.0.1:8000/download"
        r = requests.get(url)

        self.assertEqual(r.status_code, 200)
