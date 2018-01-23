# -*- coding: utf-8 -*-

from unittest import TestCase

from lib.core.downloader import Downloader
from lib.core.errors import InvalidDateError


class TestDownloader(TestCase):
    def setUp(self):
        pass

    def test_download(self):
        bread = Downloader.get_bread(2016, 9, 3)

        self.assertEqual(
            [
                bread.year, bread.month, bread.day,
                bread.book, bread.chapter,
                bread.index_start, bread.index_end,
                bread.title,
                bread.verses[0][:3], bread.verses[-1][:4],
                bread.comments[0][:4], bread.comments[-1][:3],
                bread.application,
                bread.oneword,
                bread.thoughts
            ],
            [
                2016, 9, 3,
                u'민수기', 2,
                1, 34,
                u'기를 따라 행진할지니라',
                u'여호와', u'이스라엘',
                u'하나님은', u'군대의',
                u'하나님의 군대로 부르심을 받았습니까?',
                u'자기 위치에서 주님이 주신 깃발을 따라 행진',
                u''
            ]
        )

    def test_invalid_date(self):
        def download():
            bread = Downloader.get_bread(9999, 9, 9)

        self.assertRaises(InvalidDateError, download)

    def tearDown(self):
        pass
