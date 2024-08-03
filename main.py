from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, QComboBox, QLabel, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QGridLayout,
                             QMessageBox)
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class DataBase:
    def __init__(self, db_path="database.db"):
        self.connection = None
        self.db_path = db_path

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)
        return self.connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.resize(800, 600)
        self.setStyleSheet("QPushButton { background-color: green }")

        # Add MenuBar
        file_menu_bar = self.menuBar().addMenu("&File")
        edit_menu_bar = self.menuBar().addMenu("&Edit")
        help_menu_bar = self.menuBar().addMenu("&Help")

        # Add Actions
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert_student)
        file_menu_bar.addAction(add_student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about_app)
        help_menu_bar.addAction(about_action)

        search_action = QAction(QIcon("icons/search.png"), "Search Student", self)
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

        # Add StatusBar
        self.statusbar = QStatusBar()
        self.table.cellClicked.connect(self.statusbar_widgets)

    def about_app(self):
        dialog = AboutDialog()
        dialog.exec()

    def statusbar_widgets(self):
        self.setStatusBar(self.statusbar)
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_student)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_student)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        conn = DataBase().connect()
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

    def edit_student(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_student(self):
        dialog = DeleteDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setStyleSheet("QPushButton { background-color: green }")
        content = """
        A desktop PyQt6 GUI app for managing 
        university student data with an SQL database backend.
        Feel free to modify and reuse it.
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.resize(300, 300)
        self.setStyleSheet("QPushButton { background-color: green }")
        vbox = QVBoxLayout()

        # Get index of the selected row
        index = window.table.currentRow()

        # Get the student name from selected row
        name_student = window.table.item(index, 1).text()

        self.name_line_edit = QLineEdit(name_student)
        self.name_line_edit.setPlaceholderText("Name")
        vbox.addWidget(self.name_line_edit)

        # Get the course name from selected row
        course_name = window.table.item(index, 2).text()

        self.courses = QComboBox()
        course_names = ["Biology", "Math", "Astronomy", "Physics"]
        self.courses.addItems(course_names)
        self.courses.setCurrentText(course_name)
        vbox.addWidget(self.courses)

        # Get the mobile text frm selected row
        mobile = window.table.item(index, 3).text()

        self.mobile_line_edit = QLineEdit(mobile)
        self.mobile_line_edit.setPlaceholderText("Mobile No")
        vbox.addWidget(self.mobile_line_edit)

        submit_button = QPushButton("Update")
        submit_button.clicked.connect(self.update_student)
        vbox.addWidget(submit_button)

        # Get the id text from selected row
        self.id_num = window.table.item(index, 0).text()

        self.setLayout(vbox)

    def update_student(self):
        conn = DataBase().connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.name_line_edit.text().title(),
                        self.courses.currentText(),
                        self.mobile_line_edit.text(),
                        self.id_num))
        conn.commit()
        cursor.close()
        conn.close()
        window.load_data()
        self.close()

        confirmation_box = QMessageBox()
        confirmation_box.setWindowTitle("Updated")
        confirmation_box.setText("The record has been updated successfully.")
        confirmation_box.exec()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        self.setStyleSheet("QPushButton { background-color: green }")
        layout = QGridLayout()

        message = QLabel("Are you sure you wanna delete this record?")
        layout.addWidget(message)

        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.delete_student)
        layout.addWidget(yes_button)

        no_button = QPushButton("No")
        no_button.clicked.connect(self.delete_window)
        layout.addWidget(no_button)

        self.setLayout(layout)

    def delete_student(self):
        index = window.table.currentRow()
        id_num = window.table.item(index, 0).text()

        conn = DataBase().connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id = ?", (id_num, ))
        conn.commit()
        cur.close()
        conn.close()
        window.load_data()
        self.close()

        confirmation_box = QMessageBox()
        confirmation_box.setWindowTitle("Deleted")
        confirmation_box.setText("The record has been deleted successfully from the database.")
        confirmation_box.exec()

    def delete_window(self):
        self.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.resize(300, 300)
        self.setStyleSheet("QPushButton { background-color: green }")
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
        name = name.title()
        course = self.courses.currentText()
        mobile = self.mobile_line_edit.text()

        conn = DataBase().connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO students(name, course, mobile) VALUES (?, ?, ?)",
                    (name, course, mobile))
        conn.commit()
        cur.close()
        conn.close()
        window.load_data()
        self.close()

        confirmation_box = QMessageBox()
        confirmation_box.setWindowTitle("Inserted")
        confirmation_box.setText("The record has been inserted successfully.")
        confirmation_box.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.resize(300, 300)
        self.setStyleSheet("QPushButton { background-color: green }")
        vbox = QVBoxLayout()
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
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("QStatusBar::item { border: 0px solid black };")
    window = MainWindow()
    window.load_data()
    window.show()
    sys.exit(app.exec())