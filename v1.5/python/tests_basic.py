import unittest
import app


class MyTestCase(unittest.TestCase):
    def test_anime_progress(self):
        actual = app.anime_progress("Gintama")
        expected = ('57', '201')

        self.assertEquals(actual, expected)

    def test_anime_exists_1(self):
        actual = app.anime_exists("Tower of God")
        expected = True

        self.assertEquals(actual, expected)

    def test_anime_exists_2(self):
        actual = app.anime_exists("Apple")
        expected = False

        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
