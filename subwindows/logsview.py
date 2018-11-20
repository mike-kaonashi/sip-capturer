import threading
import time
import traceback
from threading import Thread
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QScrollArea, QHBoxLayout, QFormLayout, QLabel, QLineEdit, QComboBox, QPushButton, \
    QVBoxLayout, QPlainTextEdit, QGroupBox


class Capturer(QWidget):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.sip_container = SIPContainer()
        self.log_manager = LogManager()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.log_manager)
        self.layout.addWidget(self.sip_container)


class LogManager(QWidget):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.filter_area = Filter()
        self.action_area = ActionArea()
        self.layout.addWidget(self.filter_area)
        self.layout.addWidget(self.action_area)


class Filter(QWidget):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.reset_btn = QPushButton("Reset")
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.stop_btn)
        self.layout.addWidget(self.reset_btn)
        # self.setLayout(self.layout)


class SIPContainer(QScrollArea):
    save_log_signal = pyqtSignal()

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.plain_logs = QPlainTextEdit()
        self.plain_logs.setReadOnly(True)
        self.plain_logs.setStyleSheet("background-color:black;color:white;border: 2px solid #ddd;")
        self.setStyleSheet("background-color: darkgrey;outline: 1px solid slategrey;")
        self.layout.addWidget(self.plain_logs)


