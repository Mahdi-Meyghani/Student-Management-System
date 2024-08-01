from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout)
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.resize(800, 600)

        file_menu_bar = self.menuBar().addMenu("&File")
        help_menu_bar = self.menuBar().addMenu("&Help")
        edit_menu_bar = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert_student)
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

    def insert_student(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.resize(300, 300)
        vbox = QVBoxLayout()

        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText("Name")
        vbox.addWidget(self.name_line_edit)

        self.courses = QComboBox()
        course_names = ["Biology", "Math", "Astronomy", "Physics"]
        self.courses.addItems(course_names)
        vbox.addWidget(self.courses)

        self.mobile_line_edit = QLineEdit()
        self.mobile_line_edit.setPlaceholderText("Mobile No")
        vbox.addWidget(self.mobile_line_edit)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_student)
        vbox.addWidget(submit_button)

        self.setLayout(vbox)

    def add_student(self):
        name = self.name_line_edit.text()
        course = self.courses.currentText()
        mobile = self.mobile_line_edit.text()

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO students(name, course, mobile) VALUES (?, ?, ?)",
                    (name, course, mobile))
        conn.commit()
        cur.close()
        conn.close()
        window.load_data()


app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())