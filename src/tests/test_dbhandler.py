from unittest import TestCase

from lib.core.bread import Bread
from lib.core.dbhandler import DBHandler
from lib.core.errors import DBLookupError


class TestDBHandler(TestCase):
    def setUp(self):
        self.bread = Bread(year=0, month=3, day=1)

    def test_store_and_lookup(self):
        DBHandler.store_bread(self.bread)
        bread = DBHandler.lookup_bread(0, 3, 1)
        self.assertEqual(bread.month, 3)
        self.assertEqual(bread.day, 1)

    def test_store_and_delete(self):
        def lookup():
            bread = DBHandler.lookup_bread(0, 3, 1)

        DBHandler.store_bread(self.bread)
        DBHandler.delete_bread(0, 3, 1)
        self.assertRaises(DBLookupError, lookup)

    def test_get_dates(self):
        DBHandler.store_bread(Bread(year=0, month=2, day=1))
        DBHandler.store_bread(Bread(year=0, month=4, day=2))
        DBHandler.store_bread(Bread(year=0, month=6, day=3))

        list_dates = DBHandler.get_dates()

        self.assertIn((0, 2, 1), list_dates)
        self.assertIn((0, 4, 2), list_dates)
        self.assertIn((0, 6, 3), list_dates)

        DBHandler.delete_bread(0, 2, 1)
        DBHandler.delete_bread(0, 4, 2)
        DBHandler.delete_bread(0, 6, 3)

    def tearDown(self):
        DBHandler.run_command(
            'DELETE FROM storage WHERE SUBSTR(date, 1, 4)=\'0000\''
        )
