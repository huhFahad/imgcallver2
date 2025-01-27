#message.py

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

def show_message(title, message, seconds=2):
    """ Display a message box with the specified title and message """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(title)
    msg.setText(message)
    QTimer.singleShot(seconds*1000, msg.close)
    msg.exec_()