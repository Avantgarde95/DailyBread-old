import json


class Bread(object):
    __slots__ = (
        'year', 'month', 'day',
        'book', 'chapter',
        'index_start', 'index_end',
        'title', 'verses',
        'comments', 'application', 'oneword',
        'thoughts'
    )

    def __init__(self,
                 year=0, month=0, day=0,
                 book=u'',
                 chapter=0,
                 index_start=0, index_end=0,
                 title=u'',
                 verses=(u'',),
                 comments=(u''),
                 application=u'',
                 oneword=u'',
                 thoughts=u''):
        self.year, self.month, self.day = year, month, day
        self.book = book
        self.chapter = chapter
        self.index_start, self.index_end = index_start, index_end
        self.title = title
        self.verses = list(verses)
        self.comments = list(comments)
        self.application = application
        self.oneword = oneword
        self.thoughts = thoughts

    def to_dict(self):
        return dict((key, getattr(self, key)) for key in self.__slots__)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_str(self):  # for debugging
        return u'[Date] %04d.%02d.%02d\n' \
               u'[Part] %s %d:%02d - %02d\n' \
               u'[Title] %s\n' \
               u'[Verses] \n%s\n' \
               u'[Comments] \n%s\n' \
               u'[Application] %s\n' \
               u'[Oneword] %s\n' \
               u'[Thoughts] %s' % (
                   self.year, self.month, self.day,
                   self.book, self.chapter, self.index_start, self.index_end,
                   self.title,
                   u'\n'.join(
                       u'%02d. %s' % (i, self.verses[i - self.index_start])
                       for i in xrange(self.index_start, self.index_end + 1)
                   ),
                   u'\n'.join(self.comments),
                   self.application,
                   self.oneword,
                   self.thoughts
               )
