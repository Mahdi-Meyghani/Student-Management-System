from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_bar = self.menuBar().addMenu("&File")
        help_menu_bar = self.menuBar().addMenu("&Help")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())