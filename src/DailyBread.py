# -*- coding: utf-8 -*-

import sys

# --------------------------------
# try to import Tkinter first

try:
    import Tkinter as tk
except ImportError:
    msg = u'에러 : Tkinter 모듈을 로딩하는데에 실패했습니다. 프로그램을' \
          u' 다시 설치해보세요. (Python 소스파일을 직접 실행하시는 경우 Tkinter가' \
          u' 제대로 설치되어 있는지 확인해보세요.)'

    try:
        print msg
    except UnicodeEncodeError:
        print msg.encode('utf-8')

    sys.exit(1)

# --------------------------------
# see whether data is at the right directory

from lib.core.errors import DataLoadError

try:
    import lib.core.data
except DataLoadError as e:
    msg = u'에러 : 파일 %s을 찾지 못했습니다. 해당 파일이 data 폴더가' \
          u' 아닌 다른 곳으로 이동되었는지 확인해보시고, 만일' \
          u' 파일이 손상되었거나 삭제되었을 경우 프로그램을' \
          u' 새 버전으로 따로 다운받아 해당 파일을 교체해' \
          u' 보십시오.' % str(e)

    try:
        print msg
    except UnicodeEncodeError:
        print msg.encode('utf-8')

    sys.exit(1)

# --------------------------------
# load the app

from lib.ui.editor import Editor


def main():
    root = tk.Tk()
    app = Editor(root)
    app.pack(expand=tk.YES, fill=tk.BOTH)
    root.minsize(300, 300)
    root.mainloop()


if __name__ == '__main__':
    main()
