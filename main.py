from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar)
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.resize(800, 600)

        # Add MenuBar
        file_menu_bar = self.menuBar().addMenu("&File")
        help_menu_bar = self.menuBar().addMenu("&Help")
        edit_menu_bar = self.menuBar().addMenu("&Edit")

        # Add Actions
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert_student)
        file_menu_bar.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_bar.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search_student)
        edit_menu_bar.addAction(search_action)

        # Add ToolBar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.setMovable(True)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create Table
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

    def search_student(self):
        dialog = SearchDialog()
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


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        vbox = QVBoxLayout()
        self.resize(300, 300)
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setPlaceholderText("Name")
        vbox.addWidget(self.name_line_edit)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.find_student)
        vbox.addWidget(search_button)

        self.setLayout(vbox)

    def find_student(self):
        name = self.name_line_edit.text().title()
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            window.table.item(item.row(), 1).setSelected(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.load_data()
    window.show()
    sys.exit(app.exec())