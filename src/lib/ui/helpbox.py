# -*- coding: utf-8 -*-

import Tkinter as tk

from lib.core.data import Data


class HelpBox(tk.Frame, object):
    def __init__(self, root=None):
        self.root = root
        self.style = Data.style['helpbox']
        self.str_help = Data.help
        self.image_icon = tk.PhotoImage(data=Data.icon)

        super(HelpBox, self).__init__(self.root)

        self.root.wm_title(u'도움말')
        self.root.protocol('WM_DELETE_WINDOW', self.callback_quit)
        self.root.resizable(0, 0)

        # ---------------------------------------------
        # frames

        self.frame_help = tk.Frame(self)
        self.frame_control = tk.Frame(self)

        self.frame_help.pack(padx=5, pady=3)
        self.frame_control.pack(padx=5, pady=3)

        self.frame_help.pack_propagate(False)

        # ---------------------------------------------
        # help

        self.text_help = tk.Text(self.frame_help)
        self.scrollbar_help = tk.Scrollbar(self.frame_help)

        self.scrollbar_help.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.Y)
        self.text_help.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        self.text_help.configure(yscrollcommand=self.scrollbar_help.set)
        self.scrollbar_help.configure(command=self.text_help.yview)

        # ---------------------------------------------
        # control

        self.button_quit = tk.Button(
            self.frame_control,
            text=u'     확인     ',
            command=self.callback_quit
        )

        self.button_quit.pack()

        # ---------------------------------------------
        # configuration

        self.frame_help.configure(
            width=self.style['text']['help']['width'],
            height=self.style['text']['help']['height']
        )

        self.text_help.configure(
            bg=self.style['str']['help']['bg']
        )

        self.text_help.tag_configure(
            'help',
            font=(self.style['str']['help']['font'],
                  self.style['str']['help']['size'],
                  self.style['str']['help']['style']),
            background=self.style['str']['help']['bg'],
            foreground=self.style['str']['help']['fg']
        )

        # ---------------------------------------------
        # strs

        self.text_help.insert('1.0', self.str_help, 'help')
        self.text_help.configure(state=tk.DISABLED)

        # ---------------------------------------------
        # bindings

        self.root.bind('<Escape>', self.callback_quit)

    # -------------------------------------------------------------
    # callbacks

    def callback_quit(self, *args, **kwargs):
        self.root.destroy()

    # -------------------------------------------------------------
    # overrides

    def pack(self, *args, **kwargs):
        super(HelpBox, self).pack(*args, **kwargs)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.image_icon)
