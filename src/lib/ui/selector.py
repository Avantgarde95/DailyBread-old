# -*- coding: utf-8 -*-

import Tkinter as tk
import tkMessageBox

from lib.core.data import Data
from lib.core.timetools import Timetools
from lib.core.dbhandler import DBHandler
from lib.core.errors import DBKeyListError


class Selector(tk.Frame, object):
    def __init__(self, root=None):
        self.root = root
        self.style = Data.style['selector']
        self.image_icon = tk.PhotoImage(data=Data.icon)

        super(Selector, self).__init__(self.root)

        self.root.wm_title(u'양식 찾기')
        self.root.protocol('WM_DELETE_WINDOW', self.callback_quit)
        self.root.resizable(0, 0)

        # -----------------------------------------------
        # frames

        self.frame_calendar = tk.Frame(self)
        self.frame_control = tk.Frame(self)

        self.frame_calendar.pack()
        self.frame_control.pack(pady=3)

        self.frame_header = tk.Frame(self.frame_calendar)
        self.frame_board = tk.Frame(self.frame_calendar)

        self.frame_header.pack(expand=tk.YES, fill=tk.BOTH)
        self.frame_board.pack()

        # -----------------------------------------------
        # header

        self.label_header = tk.Label(self.frame_header, text=u'0000년 00월')

        self.button_prev = tk.Button(
            self.frame_header, text=u'\u25C0', command=self.callback_prev
        )

        self.button_next = tk.Button(
            self.frame_header, text=u'\u25B6', command=self.callback_next
        )

        self.button_prev.pack(side=tk.LEFT, padx=10)
        self.label_header.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.button_next.pack(side=tk.RIGHT, padx=10)

        # -----------------------------------------------
        # board

        self.canvas_board = tk.Canvas(self.frame_board)
        self.canvas_board.pack()

        # -----------------------------------------------
        # control

        self.button_ok = tk.Button(
            self.frame_control,
            text=u'     확인     ',
            command=self.callback_ok
        )

        self.button_cancel = tk.Button(
            self.frame_control,
            text=u'     취소     ',
            command=self.callback_cancel
        )

        self.button_ok.pack(side=tk.LEFT, padx=15)
        self.button_cancel.pack(side=tk.RIGHT, padx=15)

        # -----------------------------------------------
        # configuration

        self.frame_header.configure(
            bg=self.style['label']['header']['bg']
        )

        self.label_header.configure(
            height=2,
            font=(self.style['label']['header']['font'],
                  self.style['label']['header']['size'],
                  self.style['label']['header']['style']),
            bg=self.style['label']['header']['bg'],
            fg=self.style['label']['header']['fg']
        )

        self.canvas_board.configure(
            width=self.style['canvas']['board']['cell_width'] * 7,
            height=self.style['canvas']['board']['cell_height'] * 7,
            highlightthickness=0
        )

        # -----------------------------------------------
        # canvas items

        map_weekdays = [u'일', u'월', u'화', u'수', u'목', u'금', u'토']

        self.bg_weekdays = [None] * 7
        self.str_weekdays = [None] * 7
        self.bg_days = [[None] * 7 for i in xrange(6)]
        self.str_days = [[None] * 7 for i in xrange(6)]
        self.bg_checks = [[None] * 7 for i in xrange(6)]

        w = self.style['canvas']['board']['cell_width']
        h = self.style['canvas']['board']['cell_height']

        for i in xrange(7):
            self.bg_weekdays[i] = self.canvas_board.create_rectangle(
                w * i, 0, w * (i + 1), h,
                fill=self.style['item']['weekdays']['bg'],
                outline=''
            )

            self.str_weekdays[i] = self.canvas_board.create_text(
                w * i + w / 2, h / 2,
                text=map_weekdays[i],
                font=(self.style['item']['weekdays']['font'],
                      self.style['item']['weekdays']['size'],
                      self.style['item']['weekdays']['style']),
                fill=self.style['item']['weekdays']['fg']
            )

        for i in xrange(6):
            for j in xrange(7):
                self.bg_days[i][j] = self.canvas_board.create_rectangle(
                    w * j, h * (i + 1), w * (j + 1), h * (i + 2),
                    fill=self.style['item']['days']['bg'],
                    outline=''
                )

                self.bg_checks[i][j] = (
                    self.canvas_board.create_line(
                        w * j + w / 4, h * (i + 1) + (h * 3) / 8,
                        w * j + w / 2, h * (i + 1) + (h * 3) / 4,
                        fill=self.style['item']['checks']['bg'],
                        width=3
                    ),
                    self.canvas_board.create_line(
                        w * j + w / 2, h * (i + 1) + (h * 3) / 4,
                        w * j + (w * 3) / 4, h * (i + 1) + h / 4,
                        fill=self.style['item']['checks']['bg'],
                        width=3
                    )
                )

                self.str_days[i][j] = self.canvas_board.create_text(
                    w * j + w / 2, h * (i + 1) + h / 2,
                    text='00',
                    font=(self.style['item']['days']['font'],
                          self.style['item']['days']['size'],
                          self.style['item']['days']['style']),
                    fill=self.style['item']['days']['fg']
                )

        # -----------------------------------------------
        # bindings

        self.canvas_board.bind('<ButtonPress-1>', self.callback_select)

        self.root.bind('<Return>', self.callback_ok)
        self.root.bind('<Escape>', self.callback_quit)

        self.root.bind('<Left>', self.callback_move_left)
        self.root.bind('<Right>', self.callback_move_right)
        self.root.bind('<Up>', self.callback_move_up)
        self.root.bind('<Down>', self.callback_move_down)

        # -----------------------------------------------
        # initialization

        try:
            self.dates_checked = DBHandler.get_dates()
        except DBKeyListError:
            tkMessageBox.showerror(
                'DailyBread',
                u'저장소에 저장된 날짜 목록을 불러오는데에 실패했습니다.'
                u' 저장소 파일(storage.db)이 손상되었을 수 있습니다.'
            )

        self.year, self.month, self.day = Timetools.get_today()
        self.table_days = [[0] * 7 for i in xrange(6)]
        self.coor_selected = (0, 0)
        self.result = None

        self.update_table()
        self.update_header()
        self.update_board()

        self.select_day(*self.get_ij(self.day))

    # --------------------------------------------------------------
    # callbacks

    def callback_select(self, event):
        x, y = event.x, event.y
        w = self.style['canvas']['board']['cell_width']
        h = self.style['canvas']['board']['cell_height']

        if x <= 0 or y <= h or x >= w * 7 or y >= h * 7:
            return

        i, j = y / h - 1, x / w

        if self.table_days[i][j] == 0:
            return

        self.select_day(i, j)

    def callback_prev(self):
        if self.month == 1:
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1

        self.day = 1

        self.update_table()
        self.update_header()
        self.update_board()

        self.select_day(*self.get_ij(self.day))

    def callback_next(self):
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1

        self.day = 1

        self.update_table()
        self.update_header()
        self.update_board()

        self.select_day(*self.get_ij(self.day))

    def callback_ok(self, *args, **kwargs):
        self.result = (self.year, self.month, self.day)
        self.root.destroy()

    def callback_cancel(self, *args, **kwargs):
        self.result = None
        self.root.destroy()

    def callback_quit(self, *args, **kwargs):
        self.callback_cancel()

    def callback_move_left(self, *args, **kwargs):
        i, j = self.coor_selected
        j -= 1

        if j < 0:
            return

        if self.table_days[i][j] == 0:
            return

        self.select_day(i, j)

    def callback_move_right(self, *args, **kwargs):
        i, j = self.coor_selected
        j += 1

        if j > 6:
            return

        if self.table_days[i][j] == 0:
            return

        self.select_day(i, j)

    def callback_move_up(self, *args, **kwargs):
        i, j = self.coor_selected
        i -= 1

        if i < 0:
            return

        if self.table_days[i][j] == 0:
            return

        self.select_day(i, j)

    def callback_move_down(self, *args, **kwargs):
        i, j = self.coor_selected
        i += 1

        if i > 5:
            return

        if self.table_days[i][j] == 0:
            return

        self.select_day(i, j)

    # --------------------------------------------------------------
    # component updaters

    def update_table(self):
        self.table_days = Timetools.get_calendar(self.year, self.month)

    def update_header(self):
        self.label_header.configure(
            text=u'%04d년 %02d월' % (self.year, self.month)
        )

    def update_board(self):
        for i in xrange(6):
            for j in xrange(7):
                # check the day if it is in self.dates_checked
                if ((self.year, self.month, self.table_days[i][j])
                    in self.dates_checked):
                    self.canvas_board.itemconfigure(
                        self.bg_checks[i][j][0],
                        state='normal'
                    )

                    self.canvas_board.itemconfigure(
                        self.bg_checks[i][j][1],
                        state='normal'
                    )
                else:
                    self.canvas_board.itemconfigure(
                        self.bg_checks[i][j][0],
                        state='hidden'
                    )

                    self.canvas_board.itemconfigure(
                        self.bg_checks[i][j][1],
                        state='hidden'
                    )

                # update the text of each day
                if self.table_days[i][j] == 0:
                    self.canvas_board.itemconfigure(
                        self.str_days[i][j],
                        text=''
                    )
                else:
                    self.canvas_board.itemconfigure(
                        self.str_days[i][j],
                        text='%02d' % self.table_days[i][j]
                    )

    # --------------------------------------------------------------
    # helper functions

    def select_day(self, i, j):
        i_prev, j_prev = self.coor_selected

        self.canvas_board.itemconfigure(
            self.bg_days[i_prev][j_prev],
            fill=self.style['item']['days']['bg']
        )

        self.canvas_board.itemconfigure(
            self.str_days[i_prev][j_prev],
            fill=self.style['item']['days']['fg']
        )

        self.canvas_board.itemconfigure(
            self.bg_days[i][j],
            fill=self.style['item']['days']['bg_highlight']
        )

        self.canvas_board.itemconfigure(
            self.str_days[i][j],
            fill=self.style['item']['days']['fg_highlight']
        )

        self.coor_selected = (i, j)
        self.day = self.get_day(i, j)

    def get_ij(self, day):
        if 1 in self.table_days[0]:
            num_skips = self.table_days[0].index(1)
        else:
            num_skips = 7

        i, j = divmod(num_skips + day - 1, 7)
        return i, j

    def get_day(self, i, j):
        return self.table_days[i][j]

    # --------------------------------------------------------------
    # overrides

    def pack(self, *args, **kwargs):
        super(Selector, self).pack(*args, **kwargs)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.image_icon)
