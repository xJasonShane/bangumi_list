import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parser import parse_anime_info, get_anime_list
from config import ANIME_PROPERTIES


class TestParser(unittest.TestCase):
    def setUp(self):
        self.mock_collection = {
            "subject": {
                "name": "Test Anime",
                "name_cn": "测试番剧",
                "eps": 12,
                "volumes": 1,
                "date": "2024-01-01",
                "score": 8.5,
                "type": 1,
                "collection_total": 10000,
                "rank": 100
            },
            "type": 3,
            "rate": 9
        }

    def test_parse_anime_info(self):
        anime_info = parse_anime_info(self.mock_collection)

        self.assertEqual(anime_info["番剧名"], "Test Anime")
        self.assertEqual(anime_info["中文名"], "测试番剧")
        self.assertEqual(anime_info["话数"], 12)
        self.assertEqual(anime_info["卷数"], 1)
        self.assertEqual(anime_info["发售日"], "2024-01-01")
        self.assertEqual(anime_info["评分"], 8.5)
        self.assertEqual(anime_info["用户评分"], 9)
        self.assertEqual(anime_info["类型"], "TV")
        self.assertEqual(anime_info["状态"], "已看")
        self.assertEqual(anime_info["总收藏数"], 10000)
        self.assertEqual(anime_info["排名"], 100)

    def test_parse_anime_info_missing_chinese_name(self):
        collection = self.mock_collection.copy()
        collection["subject"]["name_cn"] = ""
        anime_info = parse_anime_info(collection)
        self.assertEqual(anime_info["中文名"], "Test Anime")

    def test_get_anime_list(self):
        collections = [self.mock_collection, self.mock_collection]
        anime_list = get_anime_list(collections)
        self.assertEqual(len(anime_list), 2)
        self.assertTrue(all(prop in anime_list[0] for prop in ANIME_PROPERTIES))


if __name__ == "__main__":
    unittest.main()
