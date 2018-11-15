import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QApplication, QStackedWidget
from subwindows.logsview import LogManager, SIPContainer, Capturer


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
        #self.stack.addWidget(QWidget)
        self.layout = QVBoxLayout(self._widget)
        self.layout.addWidget(self.stack)
        self.setCentralWidget(self._widget)
        self.setFixedHeight(400)
        self.setFixedWidth(640)
        self.show()
        #self.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())