from All import MainWindow
from PySide6.QtWidgets import QApplication
import sys
from MainWindow import Ui_My_App
from PySide6 import QtWidgets
from PySide6.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


def main():
    
    app = QApplication([])
    x=MainWindow(None)
    sys.exit(app.exec())

main()