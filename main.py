from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_bar = self.menuBar().addMenu("&File")
        help_menu_bar = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu_bar.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_bar.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile No"))

        self.setCentralWidget(self.table)

    def load_data(self):
        pass


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())