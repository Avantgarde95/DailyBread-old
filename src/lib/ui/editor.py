# -*- coding: utf-8 -*-

from __future__ import with_statement
import sys
import os
import Tkinter as tk
import tkMessageBox
import tkFileDialog

from lib.core.data import Data
from lib.core.bread import Bread
from lib.core.timetools import Timetools
from lib.core.dbhandler import DBHandler
from lib.core.downloader import Downloader
from lib.core.siteopener import SiteOpener
from lib.core.errors import *

from lib.ui.helpbox import HelpBox
from lib.ui.infobox import InfoBox
from lib.ui.selector import Selector


class Editor(tk.Frame, object):
    def __init__(self, root=None):
        self.root = root
        self.style = Data.style['editor']
        self.image_icon = tk.PhotoImage(data=Data.icon)
        self.image_logo = tk.PhotoImage(data=Data.logo)

        super(Editor, self).__init__(self.root)

        self.root.wm_title(u'DailyBread')
        self.root.protocol('WM_DELETE_WINDOW', self.callback_quit)

        self.init_menus()
        self.init_frames()
        self.init_widgets()
        self.init_styles()
        self.init_binds()

        self.bread = Bread()
        self.thoughts_prev = self.bread.thoughts

    # -------------------------------------------------------------------------------------------
    # UI design

    def init_menus(self):
        self.menu_main = tk.Menu(self, tearoff=0)
        self.root.configure(menu=self.menu_main)

        self.menu_file = tk.Menu(self.menu_main, tearoff=0)
        self.menu_main.add_cascade(label=u'파일', menu=self.menu_file)

        self.menu_file.add_command(
            label=u'오늘의 양식',
            command=self.callback_bread_today,
            accelerator='Ctrl+T'
        )

        self.menu_file.add_command(
            label=u'양식 찾기',
            command=self.callback_bread_find,
            accelerator='Ctrl+O'
        )

        self.menu_file.add_command(
            label=u'양식 저장',
            command=self.callback_bread_save,
            accelerator='Ctrl+S',
        )

        self.menu_file.add_command(
            label=u'양식 삭제',
            command=self.callback_bread_delete,
            accelerator='Ctrl+R'
        )

        self.menu_file.add_command(
            label=u'양식 내보내기',
            command=self.callback_bread_export,
            accelerator='Ctrl+E'
        )

        self.menu_file.add_separator()

        self.menu_file.add_command(
            label=u'종료',
            command=self.callback_quit,
            accelerator='Esc'
        )

        self.menu_help = tk.Menu(self.menu_main, tearoff=0)
        self.menu_main.add_cascade(label=u'도움말', menu=self.menu_help)

        self.menu_help.add_command(
            label=u'도움말',
            command=self.callback_help,
            accelerator='Ctrl+P'
        )

        self.menu_help.add_command(
            label=u'프로그램 정보',
            command=self.callback_info,
            accelerator='Ctrl+N'
        )

        self.menu_help.add_separator()

        self.menu_help.add_command(
            label=u'성경읽기서비스...',
            command=self.callback_site_bs,
            accelerator='Ctrl+L'
        )

        self.menu_help.add_command(
            label=u'UBF 홈페이지...',
            command=self.callback_site_ubf,
            accelerator='Ctrl+M'
        )

    def init_frames(self):
        self.panedwindow_text = tk.PanedWindow(
            self,
            orient=tk.VERTICAL,
            sashwidth=6
        )

        self.frame_status = tk.Frame(self)

        self.frame_status.pack(side=tk.BOTTOM, expand=tk.NO, fill=tk.BOTH)
        self.panedwindow_text.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        # ------------------------------------------------

        self.panedwindow_bread = tk.PanedWindow(
            self.panedwindow_text,
            orient=tk.HORIZONTAL,
            sashwidth=6
        )

        self.frame_footer = tk.Frame(self.panedwindow_text)

        self.panedwindow_text.add(self.panedwindow_bread)
        self.panedwindow_text.add(self.frame_footer)

        self.panedwindow_text.paneconfigure(self.frame_footer, minsize=70)
        self.panedwindow_text.paneconfigure(self.panedwindow_bread, minsize=100)

        # ------------------------------------------------

        self.frame_bible = tk.Frame(self.panedwindow_bread)
        self.frame_review = tk.Frame(self.panedwindow_bread)

        self.panedwindow_bread.add(self.frame_bible)
        self.panedwindow_bread.add(self.frame_review)

        self.panedwindow_bread.paneconfigure(self.frame_bible, minsize=150)
        self.panedwindow_bread.paneconfigure(self.frame_review, minsize=150)

        # ------------------------------------------------

        self.frame_thoughts = tk.Frame(self.frame_footer)
        self.frame_logo = tk.Frame(self.frame_footer)

        # pack self.frame_logo first to prevent the logo from shrinking
        self.frame_logo.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.BOTH)
        self.frame_thoughts.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        # ------------------------------------------------

        # We pack these frames AFTER packing the labels, since packing
        # these frames first makes the labels shrink when we resize the
        # window.
        self.frame_bible_wrapper = tk.Frame(self.frame_bible)
        self.frame_review_wrapper = tk.Frame(self.frame_review)
        self.frame_thoughts_wrapper = tk.Frame(self.frame_thoughts)

        self.frame_bible_wrapper.pack_propagate(False)
        self.frame_review_wrapper.pack_propagate(False)
        self.frame_thoughts_wrapper.pack_propagate(False)

    def init_widgets(self):
        self.label_bible = tk.Label(
            self.frame_bible,
            text=u'말씀 읽기',
            anchor=tk.W,
            justify=tk.LEFT,
            relief=tk.GROOVE,
            borderwidth=2
        )

        self.label_bible.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)

        self.frame_bible_wrapper.pack(
            side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH
        )

        self.text_bible = tk.Text(self.frame_bible_wrapper)
        self.scrollbar_bible = tk.Scrollbar(self.frame_bible_wrapper)

        self.scrollbar_bible.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.Y)
        self.text_bible.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.text_bible.configure(yscrollcommand=self.scrollbar_bible.set)
        self.scrollbar_bible.configure(command=self.text_bible.yview)

        # ------------------------------------------------

        self.label_review = tk.Label(
            self.frame_review,
            text=u'생각하기',
            anchor=tk.W,
            justify=tk.LEFT,
            relief=tk.GROOVE,
            borderwidth=2
        )

        self.label_review.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)

        self.frame_review_wrapper.pack(
            side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH
        )

        self.text_review = tk.Text(self.frame_review_wrapper)
        self.scrollbar_review = tk.Scrollbar(self.frame_review_wrapper)

        self.scrollbar_review.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.Y)
        self.text_review.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.text_review.configure(yscrollcommand=self.scrollbar_review.set)
        self.scrollbar_review.configure(command=self.text_review.yview)

        # ------------------------------------------------

        self.label_thoughts = tk.Label(
            self.frame_thoughts,
            text=u'소감 및 기도',
            anchor=tk.W,
            justify=tk.LEFT,
            relief=tk.GROOVE,
            borderwidth=2
        )

        self.label_thoughts.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)

        self.frame_thoughts_wrapper.pack(
            side=tk.BOTTOM, expand=tk.YES, fill=tk.BOTH
        )

        self.text_thoughts = tk.Text(self.frame_thoughts_wrapper, undo=True)
        self.scrollbar_thoughts = tk.Scrollbar(self.frame_thoughts_wrapper)

        self.scrollbar_thoughts.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.Y)
        self.text_thoughts.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.text_thoughts.configure(yscrollcommand=self.scrollbar_thoughts.set)
        self.scrollbar_thoughts.configure(command=self.text_thoughts.yview)

        # ------------------------------------------------

        self.label_logo = tk.Label(
            self.frame_logo,
            image=self.image_logo,
            relief=tk.RIDGE,
            borderwidth=6
        )

        self.label_logo.pack(expand=tk.YES, fill=tk.BOTH)

        # ------------------------------------------------

        self.label_status = tk.Label(
            self.frame_status,
            text=u'DailyBread를 시작합니다.',
            relief=tk.SUNKEN,
            borderwidth=3,
            anchor=tk.W,
            justify=tk.LEFT
        )

        self.label_status.pack(expand=tk.YES, fill=tk.BOTH)

    def init_styles(self):
        self.panedwindow_text.configure(
            bg=self.style['panedwindow']['text']['bg']
        )

        self.panedwindow_bread.configure(
            bg=self.style['panedwindow']['bread']['bg']
        )

        # ------------------------------------------------

        self.label_bible.configure(
            font=(self.style['label']['bible']['font'],
                  self.style['label']['bible']['size'],
                  self.style['label']['bible']['style']),
            bg=self.style['label']['bible']['bg'],
            fg=self.style['label']['bible']['fg']
        )

        self.label_review.configure(
            font=(self.style['label']['review']['font'],
                  self.style['label']['review']['size'],
                  self.style['label']['review']['style']),
            bg=self.style['label']['review']['bg'],
            fg=self.style['label']['review']['fg']
        )

        self.label_thoughts.configure(
            font=(self.style['label']['thoughts']['font'],
                  self.style['label']['thoughts']['size'],
                  self.style['label']['thoughts']['style']),
            bg=self.style['label']['thoughts']['bg'],
            fg=self.style['label']['thoughts']['fg']
        )

        self.label_logo.configure(
            width=self.style['label']['logo']['width'],
            height=self.style['label']['logo']['height'],
            bg=self.style['label']['logo']['bg']
        )

        # ------------------------------------------------

        self.frame_bible_wrapper.configure(
            width=self.style['text']['bible']['width'],
            height=self.style['text']['bible']['height']
        )

        self.frame_review_wrapper.configure(
            width=self.style['text']['review']['width'],
            height=self.style['text']['review']['height']
        )

        self.frame_thoughts_wrapper.configure(
            width=self.style['text']['thoughts']['width'],
            height=self.style['text']['thoughts']['height']
        )

        # ------------------------------------------------

        self.text_bible.configure(
            bg=self.style['text']['bible']['bg']
        )

        self.text_bible.tag_configure(
            'date',
            font=(self.style['str']['date']['font'],
                  self.style['str']['date']['size'],
                  self.style['str']['date']['style']),
            background=self.style['str']['date']['bg'],
            foreground=self.style['str']['date']['fg']
        )

        self.text_bible.tag_configure(
            'part',
            font=(self.style['str']['part']['font'],
                  self.style['str']['part']['size'],
                  self.style['str']['part']['style']),
            background=self.style['str']['part']['bg'],
            foreground=self.style['str']['part']['fg']
        )

        self.text_bible.tag_configure(
            'title',
            font=(self.style['str']['title']['font'],
                  self.style['str']['title']['size'],
                  self.style['str']['title']['style']),
            background=self.style['str']['title']['bg'],
            foreground=self.style['str']['title']['fg']
        )

        self.text_bible.tag_configure(
            'indices',
            font=(self.style['str']['indices']['font'],
                  self.style['str']['indices']['size'],
                  self.style['str']['indices']['style']),
            background=self.style['str']['indices']['bg'],
            foreground=self.style['str']['indices']['fg']
        )

        self.text_bible.tag_configure(
            'verses',
            font=(self.style['str']['verses']['font'],
                  self.style['str']['verses']['size'],
                  self.style['str']['verses']['style']),
            background=self.style['str']['verses']['bg'],
            foreground=self.style['str']['verses']['fg']
        )

        # ------------------------------------------------

        self.text_review.configure(
            bg=self.style['text']['review']['bg']
        )

        self.text_review.tag_configure(
            'comments',
            font=(self.style['str']['comments']['font'],
                  self.style['str']['comments']['size'],
                  self.style['str']['comments']['style']),
            background=self.style['str']['comments']['bg'],
            foreground=self.style['str']['comments']['fg']
        )

        self.text_review.tag_configure(
            'application',
            font=(self.style['str']['application']['font'],
                  self.style['str']['application']['size'],
                  self.style['str']['application']['style']),
            background=self.style['str']['application']['bg'],
            foreground=self.style['str']['application']['fg']
        )

        self.text_review.tag_configure(
            'oneword',
            font=(self.style['str']['oneword']['font'],
                  self.style['str']['oneword']['size'],
                  self.style['str']['oneword']['style']),
            background=self.style['str']['oneword']['bg'],
            foreground=self.style['str']['oneword']['fg']
        )

        self.text_review.tag_configure(
            'marks',
            font=(self.style['str']['marks']['font'],
                  self.style['str']['marks']['size'],
                  self.style['str']['marks']['style']),
            background=self.style['str']['marks']['bg'],
            foreground=self.style['str']['marks']['fg']
        )

        # ------------------------------------------------

        self.text_thoughts.configure(
            font=(self.style['str']['thoughts']['font'],
                  self.style['str']['thoughts']['size'],
                  self.style['str']['thoughts']['style']),
            background=self.style['str']['thoughts']['bg'],
            foreground=self.style['str']['thoughts']['fg']
        )

    def init_binds(self):
        self.root.bind('<Escape>', self.callback_quit)

        # add support for ctrl-a / ctrl-A ("select all")
        self.text_thoughts.bind(
            '<Control-a>',
            self.callback_thoughts_selectall
        )

        self.text_thoughts.bind(
            '<Control-A>',
            self.callback_thoughts_selectall
        )

        self.root.bind('<Control-t>', self.callback_bread_today)
        self.root.bind('<Control-T>', self.callback_bread_today)

        self.root.bind('<Control-s>', self.callback_bread_save)
        self.root.bind('<Control-S>', self.callback_bread_save)

        self.root.bind('<Control-o>', self.callback_bread_find)
        self.root.bind('<Control-O>', self.callback_bread_find)

        self.root.bind('<Control-r>', self.callback_bread_delete)
        self.root.bind('<Control-R>', self.callback_bread_delete)

        self.root.bind('<Control-e>', self.callback_bread_export)
        self.root.bind('<Control-E>', self.callback_bread_export)

        self.root.bind('<Control-p>', self.callback_help)
        self.root.bind('<Control-P>', self.callback_help)

        self.root.bind('<Control-n>', self.callback_info)
        self.root.bind('<Control-N>', self.callback_info)

        self.root.bind('<Control-l>', self.callback_site_bs)
        self.root.bind('<Control-L>', self.callback_site_bs)

        self.root.bind('<Control-m>', self.callback_site_ubf)
        self.root.bind('<Control-M>', self.callback_site_ubf)

    # -------------------------------------------------------------------------------------------
    # callbacks

    def callback_bread_today(self, *args, **kwargs):
        self.update_bread(*Timetools.get_today())
        self.update_bible()
        self.update_review()
        self.update_thoughts()

    def callback_bread_find(self, *args, **kwargs):
        root_sub = tk.Toplevel()
        win_sub = Selector(root_sub)
        win_sub.pack()

        # block the editor and focus on the selector
        win_sub.focus_set()
        root_sub.transient(self.root)
        root_sub.grab_set()
        self.root.wait_window(root_sub)

        # get the result from the selector
        if win_sub.result is None:
            return

        # update the editor
        self.update_bread(*win_sub.result)
        self.update_bible()
        self.update_review()
        self.update_thoughts()

    def callback_bread_save(self, *args, **kwargs):
        self.bread.thoughts = self.text_thoughts.get('1.0', tk.END).strip()
        self.thoughts_prev = self.bread.thoughts

        try:
            DBHandler.store_bread(self.bread)
        except DBStoreError:
            self.write_status(u'에러가 발생했습니다.')

            self.raise_error(
                u'양식을 저장하는데에 실패했습니다. 저장소 파일'
                u'(storage.db)이 손상되었을 수 있습니다.'
            )

        self.write_status(u'양식을 저장소에 성공적으로 저장했습니다.')

    def callback_bread_export(self, *args, **kwargs):
        # generate the string
        contents = u'[날짜]\n%04d.%02d.%02d\n\n' \
                   u'[파트]\n%s %d장 %02d ~ %02d절\n\n' \
                   u'[제목]\n%s\n\n' \
                   u'[말씀]\n%s\n\n' \
                   u'[생각하기]\n%s\n\n' \
                   u'[적용]\n%s\n\n' \
                   u'[한마디]\n%s\n\n' \
                   u'[소감 및 기도]\n%s' % (
                       self.bread.year, self.bread.month, self.bread.day,
                       self.bread.book, self.bread.chapter,
                       self.bread.index_start, self.bread.index_end,
                       self.bread.title,
                       u'\n\n'.join(
                           u'%02d. %s' % (
                               i, self.bread.verses[i - self.bread.index_start])
                           for i in xrange(self.bread.index_start,
                                           self.bread.index_end + 1)
                       ),
                       u'\n\n'.join(self.bread.comments),
                       self.bread.application,
                       self.bread.oneword,
                       self.text_thoughts.get('1.0', tk.END)
                   )

        # generate the default file name
        filename_default = 'bread_%04d_%02d_%02d.txt' % (
            self.bread.year, self.bread.month, self.bread.day
        )

        # save the string
        path_save = tkFileDialog.asksaveasfilename(
            title=u'양식 내보내기',
            filetypes=[(u'텍스트 파일', '.txt')],
            initialfile=filename_default
        )

        if not path_save:
            self.write_status(u'양식 내보내기가 취소되었습니다.')
            return

        path_real = os.path.realpath(path_save)

        try:
            with open(path_real, 'w') as p:
                p.write(contents.encode('utf-8'))
        except (IOError, OSError):
            self.write_status(u'에러가 발생했습니다.')

            self.raise_error(
                u'파일을 저장하는데에 실패했습니다. 선택한 폴더가'
                u' 실제로 존재하는지 확인해 보십시오.'
            )

            return

        self.write_status(u'파일 %s를 성공적으로 저장했습니다.' % path_save)

    def callback_bread_delete(self, *args, **kwargs):
        flag_delete = tkMessageBox.askokcancel(
            'DailyBread',
            u'날짜 %04d.%02d.%02d의 양식을 정말로 삭제하시겠습니까? 양식을'
            u' 삭제하면 작성하신 소감이 저장소에서 삭제되며, 후에 양식을'
            u' 다시 열 때 인터넷 접속이 필요합니다.' % (
                self.bread.year, self.bread.month, self.bread.day
            )
        )

        if not flag_delete:
            self.write_status(u'양식 삭제가 취소되었습니다.')
            return

        try:
            DBHandler.delete_bread(
                self.bread.year, self.bread.month, self.bread.day
            )
        except DBDeleteError:
            self.write_status(u'에러가 발생했습니다.')
            self.raise_error(u'양식 삭제에 실패했습니다.')
            return

        self.write_status(
            u'날짜 %04d.%02d.%02d에 해당하는 양식을 저장소에서'
            u' 삭제했습니다.' % (
                self.bread.year, self.bread.month, self.bread.day
            )
        )

    def callback_help(self, *args, **kwargs):
        root_sub = tk.Toplevel()
        win_sub = HelpBox(root_sub)
        win_sub.pack()
        win_sub.focus_set()

    def callback_info(self, *args, **kwargs):
        root_sub = tk.Toplevel()
        win_sub = InfoBox(root_sub)
        win_sub.pack()
        win_sub.focus_set()

    def callback_site_bs(self, *args, **kwargs):
        try:
            SiteOpener.open_site('bs')
        except SiteOpenError:
            self.write_status(u'에러가 발생했습니다.')
            self.raise_error(
                u'웹사이트 접속에 실패했습니다. 인터넷 연결 상태를'
                u' 확인해보세요.'
            )

    def callback_site_ubf(self, *args, **kwargs):
        try:
            SiteOpener.open_site('ubf')
        except SiteOpenError:
            self.write_status(u'에러가 발생했습니다.')
            self.raise_error(
                u'웹사이트 접속에 실패했습니다. 인터넷 연결 상태를'
                u' 확인해보세요.'
            )

    def callback_quit(self, *args, **kwargs):
        try:
            if self.text_thoughts.get('1.0', tk.END).rstrip() \
                    == self.thoughts_prev.rstrip():
                flag_quit = tkMessageBox.askokcancel(
                    'Dailybread',
                    u'프로그램을 종료하시겠습니까?'
                )
            else:
                flag_quit = tkMessageBox.askokcancel(
                    'Dailybread',
                    u'소감이 수정되었지만 저장되지 않았습니다. 프로그램을'
                    u' 종료하시겠습니까?'
                )

            if flag_quit:
                self.root.destroy()
            else:
                self.write_status(u'프로그램 종료가 취소되었습니다.')
        except:
            # make sure the program is killed even when some errors occur
            sys.exit(0)

    def callback_thoughts_selectall(self, event):
        self.text_thoughts.tag_add(tk.SEL, '1.0', tk.END)
        self.text_thoughts.mark_set(tk.INSERT, '1.0')
        self.text_thoughts.see(tk.INSERT)
        return 'break'

    # -------------------------------------------------------------------------------------------
    # component updaters

    def update_bread(self, year, month, day):
        # try to load the bread from DB
        flag_stored = True

        try:
            bread = DBHandler.lookup_bread(year, month, day)
        except DBLookupError:
            bread = None  # for suppressing PyCharm warning
            flag_stored = False

        if flag_stored:
            self.write_status(
                u'저장소에서 날짜 %04d.%02d.%02d에 해당하는 양식을'
                u' 성공적으로 불러왔습니다.' % (year, month, day)
            )
            self.bread = bread
            self.thoughts_prev = self.bread.thoughts
            return

        # try to load the bread from the Internet
        try:
            bread = Downloader.get_bread(year, month, day)
        except ConnectionError:
            self.write_status(u'에러가 발생했습니다.')

            self.raise_error(
                u'웹사이트 연결에 실패했습니다. 인터넷 연결 상태를'
                u' 확인해 보십시오.'
            )

            return
        except InvalidDateError:
            self.write_status(u'에러가 발생했습니다.')

            self.raise_error(
                u'웹사이트에서 양식을 다운받는데에 실패했습니다.'
                u' 웹사이트에 아직 양식이 업데이트되지 않았을 수 있습니다.'
            )

            return

        self.bread = bread
        self.thoughts_prev = self.bread.thoughts

        self.write_status(
            u'인터넷에서 날짜 %04d.%02d.%02d에 해당하는 양식을 성공적으로'
            u' 불러왔습니다.' % (year, month, day)
        )

    def update_bible(self):
        self.text_bible.configure(state=tk.NORMAL)
        self.text_bible.delete('1.0', tk.END)

        self.text_bible.insert(
            tk.INSERT,
            u'%04d년 %02d월 %02d일\n\n' % (
                self.bread.year, self.bread.month, self.bread.day
            ),
            'date'
        )

        self.text_bible.insert(
            tk.INSERT,
            u'%s %d장 %02d ~ %02d절\n\n' % (
                self.bread.book, self.bread.chapter,
                self.bread.index_start, self.bread.index_end
            ),
            'part'
        )

        self.text_bible.insert(
            tk.INSERT,
            u'%s\n' % self.bread.title,
            'title'
        )

        for i in xrange(self.bread.index_end - self.bread.index_start + 1):
            self.text_bible.insert(
                tk.INSERT,
                u'\n%02d. ' % (i + self.bread.index_start),
                'indices'
            )

            self.text_bible.insert(
                tk.INSERT,
                u'%s\n' % self.bread.verses[i],
                'verses'
            )

        self.text_bible.configure(state=tk.DISABLED)

    def update_review(self):
        self.text_review.configure(state=tk.NORMAL)
        self.text_review.delete('1.0', tk.END)

        for c in self.bread.comments:
            self.text_review.insert(tk.INSERT, u'  %s\n\n' % c, 'comments')

        self.text_review.insert(tk.INSERT, u'적용', 'marks')

        self.text_review.insert(
            tk.INSERT,
            u'\n%s\n\n' % self.bread.application,
            'application'
        )

        self.text_review.insert(tk.INSERT, u'한마디', 'marks')

        self.text_review.insert(
            tk.INSERT,
            u'\n%s\n' % self.bread.oneword,
            'oneword'
        )

        self.text_review.configure(state=tk.DISABLED)

    def update_thoughts(self):
        self.text_thoughts.delete('1.0', tk.END)
        self.text_thoughts.insert(
            tk.INSERT,
            self.bread.thoughts
        )

    # -------------------------------------------------------------------------------------------
    # helper functions

    def raise_error(self, message):
        tkMessageBox.showerror('DailyBread', message)

    def write_status(self, message):
        self.label_status.configure(text=message)

    # -------------------------------------------------------------------------------------------
    # overrides

    def pack(self, *args, **kwargs):
        super(Editor, self).pack(*args, **kwargs)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.image_icon)

        # We initialize the app at this time to make sure that the widgets
        # are completely drawn before any error message occurs.
        self.update_bread(*Timetools.get_today())
        self.update_bible()
        self.update_review()
        self.update_thoughts()
