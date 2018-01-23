from distutils.core import setup
import py2exe
import sys

# This enables us to just run "python setup.py".
sys.argv.append('py2exe')

setup(
    name='DailyBread',
    version='1.4',
    author='Hun-Min Park',
    windows=[{
        'script': '../src/DailyBread.py'
    }],
    options={
        'build': {
            'build_base': '../build_win'
        },
        'py2exe': {
            'bundle_files': 2,
            'compressed': True,
            'optimize': 2,
            'dist_dir': '../dist_win',
            'includes': [
                'Tkinter',
                'lib'
            ],
            'dll_excludes': ['w9xpopen.exe']
        }
    }
)
