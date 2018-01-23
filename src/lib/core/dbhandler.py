import sqlite3
import json

from lib.core.bread import Bread
from lib.core.data import Data
from lib.core.errors import (DBLookupError, DBStoreError, DBDeleteError,
                             DBKeyListError)

conn = Data.conn


class DBHandler(object):
    @staticmethod
    def store_bread(bread):
        value_date = '%04d.%02d.%02d' % (bread.year, bread.month, bread.day)
        value_bread = bread.to_json()

        try:
            with conn:
                conn.execute(
                    'INSERT OR REPLACE INTO storage (date, bread)'
                    ' VALUES (?, ?)',
                    (value_date, value_bread)
                )
        except sqlite3.Error:
            raise DBStoreError

    @staticmethod
    def lookup_bread(year, month, day):
        value_date = '%04d.%02d.%02d' % (year, month, day)

        try:
            with conn:
                items = list(conn.execute(
                    'SELECT * FROM storage WHERE date=?',
                    (value_date,)
                ))
        except sqlite3.Error:
            raise DBLookupError

        if not items:
            raise DBLookupError

        try:
            data = json.loads(items[0][1])
        except ValueError:
            raise DBLookupError

        return Bread(**data)

    @staticmethod
    def delete_bread(year, month, day):
        value_date = '%04d.%02d.%02d' % (year, month, day)

        try:
            with conn:
                conn.execute(
                    'DELETE FROM storage WHERE date=?',
                    (value_date,)
                )
        except sqlite3.Error:
            raise DBDeleteError

    @staticmethod
    def get_dates():
        try:
            with conn:
                items = list(conn.execute(
                    'SELECT date FROM storage'
                ))
        except sqlite3.Error:
            raise DBKeyListError

        return [tuple(int(v) for v in values[0].split('.'))
                for values in items]

    @staticmethod
    def run_command(cmd):  # for debugging
        with conn:
            return conn.execute(cmd)
