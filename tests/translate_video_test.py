import unittest

from video_translator import VideoTranslator


class TestVideoTranslator(unittest.TestCase):
    def test_generate_subtitles_short(self):
        video_path = "./tests/data/short.mp4"
        video_translator = VideoTranslator(video_path)
        subtitles = video_translator.generate_subtitles(["en", "id", "ja"])
        self.assertEqual(subtitles.original_language, "id")
        self.assertEqual(subtitles.languages, ["en", "id", "ja"])

    def test_generate_subtitles_complete(self):
        video_path = "./tests/data/JKT48 13th Generation Profile_ Jemima.mp4"
        video_translator = VideoTranslator(video_path)
        subtitles = video_translator.generate_subtitles(["en", "id", "ja"])
        self.assertEqual(subtitles.original_language, "id")
        self.assertEqual(subtitles.languages, ["en", "id", "ja"])

    def test_generate_subtitles_7minutes(self):
        video_path = "./tests/data/48_KABUTAKE_MANA.mp4"
        video_translator = VideoTranslator(video_path)
        subtitles = video_translator.generate_subtitles(["en", "id", "ja"])
        self.assertEqual(subtitles.original_language, "id")
        self.assertEqual(subtitles.languages, ["en", "id", "ja"])
