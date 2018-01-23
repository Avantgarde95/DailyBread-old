from __future__ import with_statement
import os
import sys
import sqlite3
import json

from lib.core.errors import DataLoadError

# if frozen by pyinstaller, py2exe, etc. ...
if hasattr(sys, 'frozen'):
    path_base = os.path.dirname(os.path.realpath(sys.executable))
    path_data = os.path.join(path_base, 'data')
# otherwise...
else:
    path_base = os.path.dirname(os.path.realpath(__file__))
    path_data = os.path.join(path_base, '../../data')

# change the working directory to path_data
os.chdir(path_data)


class Data(object):
    # -------------------------------------------
    # db

    try:
        conn = sqlite3.connect('storage.db')
    except sqlite3.Error:
        raise DataLoadError('storage.db')

    # -------------------------------------------
    # style

    try:
        with open('style.json', 'r') as p:
            style = json.load(p)
    except (ValueError, IOError):
        raise DataLoadError('style.json')

    # -------------------------------------------
    # texts

    try:
        with open('info.txt', 'r') as p:
            info = p.read()
    except IOError:
        raise DataLoadError('info.txt')

    try:
        with open('help.txt', 'r') as p:
            help = p.read()
    except IOError:
        raise DataLoadError('help.txt')

    # -------------------------------------------
    # images

    try:
        with open('icon.gif', 'rb') as p:
            icon = p.read().encode('base64')
    except IOError:
        raise DataLoadError('icon.gif')

    try:
        with open('logo.gif', 'rb') as p:
            logo = p.read().encode('base64')
    except IOError:
        raise DataLoadError('logo.gif')
