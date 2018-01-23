from unittest import TestCase
import json

from lib.core.bread import Bread


class TestBread(TestCase):
    def setUp(self):
        self.bread = Bread()

    def test_dict(self):
        table = self.bread.to_dict()
        bread_converted = Bread(**table)
        self.assertEqual(self.bread.to_str(), bread_converted.to_str())

    def test_json(self):
        data = self.bread.to_json()
        bread_converted = Bread(**json.loads(data))
        self.assertEqual(self.bread.to_str(), bread_converted.to_str())

    def tearDown(self):
        pass
