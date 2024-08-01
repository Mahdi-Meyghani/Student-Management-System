from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QMainWindow,
                             QTableWidget, QTableWidgetItem)
from PyQt6.QtGui import QAction
import sys
import sqlite3


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
        self.table.verticalHeader().setVisible(False)

        self.setCentralWidget(self.table)

    def load_data(self):
        conn = sqlite3.connect("database.db")
        result = conn.execute("SELECT * FROM students")
        self.table.setRowCount(0)

        for row_index, row in enumerate(result):
            self.table.insertRow(row_index)
            for col_index, cell in enumerate(row):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(cell)))
        conn.close()


app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())