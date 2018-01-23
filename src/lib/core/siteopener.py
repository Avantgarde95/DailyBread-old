import webbrowser

from lib.core.errors import SiteOpenError

url = {
    'bs': 'http://bs.ubf.kr',
    'ubf': 'http://ubf.kr'
}


class SiteOpener(object):
    @staticmethod
    def open_site(key):
        try:
            webbrowser.open(url[key])
        except webbrowser.Error:
            raise SiteOpenError
