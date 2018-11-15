from PyQt5.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, \
    QVBoxLayout, QPlainTextEdit, QGroupBox
import time
from threading import Thread

class Capturer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(LogManager())
        self.layout.addWidget(SIPContainer())
        self.setGeometry(0, 40, 0, 0)


class LogManager(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(Filter())
        self.layout.addWidget(ActionArea())


class Filter(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.options_container = QGroupBox("Options")
        self.options_container_layout = QFormLayout()
        self.options_container.setLayout(self.options_container_layout)
        self.options_container_layout.addRow(QLabel("Host"), QLineEdit())
        self.options_container_layout.addRow(QLabel("Net"), QLineEdit())
        self.options_container_layout.addRow(QLabel("Port"), QLineEdit())

        self.directions_container = QGroupBox("Directions")
        self.directions_container_layout = QFormLayout()
        self.directions_container.setLayout(self.directions_container_layout)
        self.directions_container_layout.addRow(QLabel("Src"), QLineEdit())
        self.directions_container_layout.addRow(QLabel("Dst"), QLineEdit())
        self.proto_choices = QComboBox()
        self.proto_choices.addItem('tcp')
        self.proto_choices.addItem('udp')
        self.proto_choices.addItem('icmp')
        self.proto_choices.addItem('ah')
        self.directions_container_layout.addRow(QLabel("Proto"), self.proto_choices)

        self.layout.addWidget(self.options_container)
        self.layout.addWidget(self.directions_container)


class ActionArea(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QPushButton("Start"))
        self.layout.addWidget(QPushButton("Stop"))
        self.layout.addWidget(QPushButton("Reset"))
        #self.setLayout(self.layout)

class SIPContainer(QScrollArea):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.plain_logs = QPlainTextEdit()
        self.plain_logs.setReadOnly(True)
        self.plain_logs.setStyleSheet("background-color:black;color:white;border: 2px solid #ddd;")
        self.plain_logs.setPlainText("Hello")
        self.layout.addWidget(self.plain_logs)
        self.print_log_thread = Thread(target=self.add_text)
        self.print_log_thread.start()
        #self.print_log_thread.join()

    def add_text(self):
        count=0
        while True:
            time.sleep(1)
            self.plain_logs.setPlainText(str(count))
            count = count + 1
