import logging
import sys
import threading
import time
import traceback
from threading import Thread

from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QApplication, \
    QStackedWidget, QScrollBar, QAction, QFileDialog

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
        save_trig = QAction(QIcon('icon/diskette.png'), 'Save As ...', self)
        save_trig.setShortcut('Ctrl+S')
        exit_trig = QAction(QIcon('icon/opened-filled-door.png'), 'Exit', self)
        exit_trig.setShortcut('Ctrl+E')
        file_menu.addAction(save_trig)
        file_menu.addAction(exit_trig)

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
        self.thread_1 = SpecThread(target=self.add_text, )
        self.created_flag = False
        self.main_win.log_manager.action_area.stop_btn.setDisabled(False)
        self.main_win.log_manager.action_area.start_btn.clicked.connect(self.run_thread)
        self.main_win.log_manager.action_area.stop_btn.clicked.connect(self.stop_thread)
        self.main_win.log_manager.action_area.reset_btn.clicked.connect(self.reset_logs)
        save_trig.triggered.connect(self.save_file)
        exit_trig.triggered.connect(self.exit_app)
        print(sys.platform)

    def exit_app(self):
        #threading.
        self.close()
        sys.exit()

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def reset_logs(self):
        self.main_win.sip_container.plain_logs.setPlainText('')

    def add_text(self):
        self.main_win.sip_container.plain_logs.appendPlainText('...\n')
        scrollbar = self.main_win.sip_container.verticalScrollBar()
        assert  isinstance(scrollbar, QScrollBar)
        scrollbar.setValue(scrollbar.maximum())
        self.main_win.sip_container.plain_logs.moveCursor(QTextCursor.End)
        time.sleep(1)

    def run_thread(self):
        try:
            if not self.created_flag:
                self.thread_1.start()
                self.created_flag = True
            else:
                self.thread_1.resume()
            self.main_win.log_manager.action_area.start_btn.setDisabled(True)
            self.main_win.log_manager.action_area.stop_btn.setDisabled(False)
        except Exception as e:
            print(e)
            traceback.print_exc()

    def stop_thread(self):
        self.main_win.log_manager.action_area.start_btn.setDisabled(False)
        self.main_win.log_manager.action_area.stop_btn.setDisabled(True)
        self.thread_1.pause()

class SpecThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.paused = False
        self._return = None
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        while True:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                if self._target is not None:
                    self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return

    def pause(self):
        self.paused = True
        self.pause_cond.acquire()

    def resume(self):
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

    def terminate(self):
        ...
        #self.

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
