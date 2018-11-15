import logging
import sys
import threading
import time
import traceback
from threading import Thread

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QApplication, QStackedWidget, QScrollBar

from subwindows.logsview import Capturer


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._widget = QWidget()
        self.title = 'SIP Message Capturer'
        self.setGeometry(500, 400, 640, 400)
        self.setWindowTitle(self.title)
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        view_menu = main_menu.addMenu('View')
        self.main_win = Capturer()
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.main_win)
        # self.stack.addWidget(QWidget)
        self.layout = QVBoxLayout(self._widget)
        self.layout.addWidget(self.stack)
        self.setCentralWidget(self._widget)
        self.setFixedHeight(400)
        self.setFixedWidth(640)
        self.show()

        self.main_win.log_manager.action_area.start_btn.clicked.connect(self.run_thread)
        self.main_win.log_manager.action_area.stop_btn.clicked.connect(self.stop_thread)

    def add_text(self):
        self.main_win.sip_container.plain_logs.appendPlainText('...\n')
        scrollbar = self.main_win.sip_container.verticalScrollBar()
        assert  isinstance(scrollbar, QScrollBar)
        scrollbar.setValue(scrollbar.maximum())
        self.main_win.sip_container.plain_logs.moveCursor(QTextCursor.End)
        time.sleep(1)

    def run_thread(self):
        try:
            #print(threading.List)
            self.thread_1 = SpecThread(target=self.add_text, )
            self.thread_1.start()
        except Exception as e:
            print(e)
            traceback.print_exc()

    def stop_thread(self):
        self.thread_1.shutdown_flag.set()

class SpecThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.shutdown_flag = threading.Event()
        self._return = None

    def run(self):
        while not self.shutdown_flag.is_set():
            if self._target is not None:
                self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
