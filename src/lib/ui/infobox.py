# -*- coding: utf-8 -*-

import Tkinter as tk

from lib.core.data import Data


class InfoBox(tk.Frame, object):
    def __init__(self, root=None):
        self.root = root
        self.style = Data.style['infobox']
        self.str_info = Data.info
        self.image_icon = tk.PhotoImage(data=Data.icon)
        self.image_logo = tk.PhotoImage(data=Data.logo)

        super(InfoBox, self).__init__(self.root)

        self.root.wm_title(u'프로그램 정보')
        self.root.protocol('WM_DELETE_WINDOW', self.callback_quit)
        self.root.resizable(0, 0)

        # ----------------------------------------------
        # frames

        self.frame_logo = tk.Frame(self)
        self.frame_info = tk.Frame(self)
        self.frame_control = tk.Frame(self)

        self.frame_logo.pack(padx=5, pady=3)
        self.frame_info.pack(padx=5)
        self.frame_control.pack(padx=5, pady=3)

        self.frame_info.pack_propagate(False)

        # ----------------------------------------------
        # logo

        self.label_logo = tk.Label(
            self.frame_logo,
            image=self.image_logo
        )

        self.label_logo.pack()

        # ----------------------------------------------
        # info

        self.label_info = tk.Label(
            self.frame_info,
            text=self.str_info,
            anchor=tk.W,
            justify=tk.LEFT
        )

        self.label_info.pack(expand=tk.YES, fill=tk.BOTH)

        # ----------------------------------------------
        # control

        self.button_quit = tk.Button(
            self.frame_control,
            text=u'     확인     ',
            command=self.callback_quit
        )

        self.button_quit.pack()

        # ----------------------------------------------
        # configuration

        self.frame_info.configure(
            width=self.style['label']['info']['width'],
            height=self.style['label']['info']['height']
        )

        self.label_info.configure(
            bg=self.style['label']['info']['bg'],
            fg=self.style['label']['info']['fg'],
            font=(self.style['label']['info']['font'],
                  self.style['label']['info']['size'],
                  self.style['label']['info']['style'])
        )

        # ----------------------------------------------
        # bindings

        self.root.bind('<Escape>', self.callback_quit)

    # ------------------------------------------------------------
    # callbacks

    def callback_quit(self, *args, **kwargs):
        self.root.destroy()

    # ------------------------------------------------------------
    # overrides

    def pack(self, *args, **kwargs):
        super(InfoBox, self).pack(*args, **kwargs)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.image_icon)
