import urllib2
import HTMLParser

from lib.core.bread import Bread
from lib.core.timetools import Timetools
from lib.core.errors import ConnectionError, InvalidDateError


class Parser_dblist(HTMLParser.HTMLParser, object):
    def __init__(self):
        super(Parser_dblist, self).__init__()
        self.type_data = None
        self.data_dblist = []

    def handle_starttag(self, tag, attrs):
        if not attrs:
            return

        if tag == 'td' and attrs[0] == ('class', 'sel_maindblist'):
            self.type_data = 'dblist'

    def handle_endtag(self, tag):
        self.type_data = None

    def handle_data(self, data):
        if self.type_data == 'dblist':
            self.data_dblist.append(data)


class Parser_idinfo(HTMLParser.HTMLParser, object):
    def __init__(self):
        super(Parser_idinfo, self).__init__()
        self.data_idinfo = []

    def handle_starttag(self, tag, attrs):
        if not attrs:
            return

        if (tag == 'a'
            and attrs[0][0] == 'href'
            and attrs[0][1].startswith('/dailybread/dbdisp.php?id=')):
            id_ = int(attrs[0][1].split('=')[-1])
            self.data_idinfo.append(id_)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


class Parser_bread(HTMLParser.HTMLParser, object):
    def __init__(self):
        super(Parser_bread, self).__init__()
        self.type_data = None
        self.data_text_1 = []
        self.data_text_2 = []
        self.data_title = []
        self.data_body_1 = []
        self.data_body_2 = []

    def handle_starttag(self, tag, attrs):
        if not attrs:
            return

        if tag == 'div':
            attr_first = attrs[0]

            if attr_first == ('class', 'text1'):
                self.type_data = 'text_1'
            elif attr_first == ('class', 'text2'):
                self.type_data = 'text_2'
            elif attr_first == ('class', 'ng_title'):
                self.type_data = 'title'
            elif attr_first == ('class', 'ng_tdbbody2'):
                self.type_data = 'body_2'
            else:
                return

        if tag == 'td':
            if attrs[0] == ('class', 'ng_tdbbody1'):
                self.type_data = 'body_1'

    def handle_endtag(self, tag):
        self.type_data = None

    def handle_data(self, data):
        type_data = self.type_data

        if type_data == 'text_1':
            self.data_text_1.append(data)
        elif type_data == 'text_2':
            self.data_text_2.append(data)
        elif type_data == 'title':
            self.data_title.append(data)
        elif type_data == 'body_1':
            self.data_body_1.append(data)
        elif type_data == 'body_2':
            self.data_body_2.append(data)
        else:
            pass


class Downloader(object):
    @staticmethod
    def get_html(url):
        try:
            request = urllib2.urlopen(url)
        except urllib2.URLError:
            raise ConnectionError

        return unicode(request.read(), 'euc-kr')

    @staticmethod
    def get_bread(year, month, day):
        # ------------------------------------
        # get the newest post from the first page of dblist

        html_dblist = Downloader.get_html(
            'http://bs.ubf.kr/dailybread/dblist.php?start=0'
        )

        parser_dblist = Parser_dblist()
        parser_dblist.feed(html_dblist)

        year_newest, month_newest, day_newest = map(
            int, parser_dblist.data_dblist[1].split('.')
        )

        # ------------------------------------
        # find the index of today's bread in dblist

        index = Timetools.get_diffdays(
            year, month, day,
            year_newest, month_newest, day_newest
        )

        if index < 0:
            raise InvalidDateError

        # ------------------------------------
        # get the id of the page

        html_idinfo = Downloader.get_html(
            'http://bs.ubf.kr/dailybread/dblist.php?start=%d' % index
        )

        parser_idinfo = Parser_idinfo()
        parser_idinfo.feed(html_idinfo)

        if parser_idinfo.data_idinfo:
            id_ = parser_idinfo.data_idinfo[0]
        else:
            raise InvalidDateError

        # ------------------------------------
        # get the bread from the page

        html_bread = Downloader.get_html(
            'http://bs.ubf.kr/dailybread/dbdisp.php?id=%d' % id_
        )

        parser_bread = Parser_bread()
        parser_bread.feed(html_bread)

        bread = Bread(
            year=int(parser_bread.data_text_1[0]),
            month=int(parser_bread.data_text_2[0].split('/')[0]),
            day=int(parser_bread.data_text_2[0].split('/')[1]),
            book=parser_bread.data_title[0].split(':')[0].split()[0],
            chapter=int(parser_bread.data_title[0].split(':')[0].split()[1]),
            index_start=int(parser_bread.data_body_1[0]),
            index_end=int(parser_bread.data_body_1[-2]),
            title=parser_bread.data_title[1].strip(),
            verses=[s.strip() for s in parser_bread.data_body_1[1::2]],
            comments=[s.strip() for s in parser_bread.data_body_2[:-2]],
            application=parser_bread.data_body_2[-2].strip(),
            oneword=parser_bread.data_body_2[-1].strip()
        )

        return bread
