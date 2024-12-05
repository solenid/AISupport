import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QPushButton, QTableWidgetItem, QMainWindow, QTableWidget, \
    QHBoxLayout, QHeaderView, QVBoxLayout

from DataBaseInterface import *

def get_last_five_scans():
    result = []
    users = getLast5Users()
    for user in users:
        user_dict = {
            "scan_id": user[0],
            "first_name": user[2],
            "last_name": user[1],
            "birth_date": user[3]
        }
        result.append(user_dict)
    return result

columns = ['Дата рождения', 'ID', 'Nickname', 'Рекомендация', '']



class HistoryWindow(QWidget):
    def __init__(self):  # Исправлено на __init__
        super().__init__()

        self.scans = get_last_five_scans()

        # Создаем QTableWidget
        self.table = QTableWidget()
        self.table.setColumnCount(len(columns))
        self.table.setRowCount(0)  # Начинаем с 0 строк

        # Устанавливаем заголовки
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Заполняем таблицу данными и добавляем кнопки
        for scan in self.scans:
            self.add_scan_to_table(scan)

        self.table.setStyleSheet("""
            QTableWidget {
                font-size: 12px;
                color: #000000;
                gridline-color: #d3d3d3;
                background-color: white;
            }
            QHeaderView::section {
                background-color: white;
                color:#D53032;
                padding: 5px;
                border: 1px solid #d3d3d3;
                border-top:none;
                font-size: 12px;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)

        # Устанавливаем вертикальный layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_scan_to_table(self, scan):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Предполагается, что scan - это список или кортеж с данными
        for column, data in enumerate(scan):
            self.table.setItem(row_position, column, QTableWidgetItem(data))
    def add_scan_to_table(self, scan):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.user_details = getUserById(scan['scan_id'])

        self.table.setItem(row_position, 0, QTableWidgetItem(scan['birth_date']))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(scan['scan_id'])))
        self.table.setItem(row_position, 2, QTableWidgetItem(scan['first_name'] + " " + scan['last_name']))
        self.table.setItem(row_position, 3, QTableWidgetItem(self.user_details[9]))  # scan['СЮДА ТИПО РЕКОМЕНДАЦИЮ']

        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)

        # Создаем кнопку "Подробнее"
        button = QPushButton("Подробнее")
        button.clicked.connect(lambda checked, r=row_position: self.on_button_click(r))
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #D53032;
                padding:5px;
                color: #D53032;
                font-size: 12px;
                border-radius: 5px;
            }
        """)

        # Создаем кнопку удаления
        buttonDelete = QPushButton()
        buttonDelete.setIcon(QIcon("iconDelete.png"))  # Укажите путь к вашей иконке
        buttonDelete.clicked.connect(lambda checked, r=row_position: self.on_delete_button_click(r))

        buttonDelete.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #D53032;
            }
        """)

        button_layout.addWidget(button)
        button_layout.addWidget(buttonDelete)

        self.table.setCellWidget(row_position, 4, button_widget)

    def on_delete_button_click(self, row):
        print(f"Delete button in row {row + 1} clicked!")

        self.table.removeRow(row)  # Удаляем строку из таблицы

        print(self.table.rowCount())

        if self.table.rowCount() == 0:
            self.table.setRowCount(0)
            print("Таблица теперь пуста.")



    def on_button_click(self, row):
        print(f"Button in row {row + 1} clicked!")
        self.scanId = self.scans[row]['scan_id']
        try:
            self.scanId = int(self.scanId)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный ID скана.")
            return
        self.HistoryDetailWindow = HistoryDetailWindow(self.scanId)
        self.HistoryDetailWindow.show()



class HistoryDetailWindow(QMainWindow):
    def __init__(self, scanId):
        super().__init__()

        self.setWindowTitle('HR SOLUTION')
        self.resize(800, 600)
        self.setStyleSheet("""
            background-color: #ffffff;
        """)

        self.scanId = scanId
        self.user_details = getUserById(scanId)
        if self.user_details:
            # Создаем центральный виджет и основной вертикальный макет
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)

            # Убираем отступы
            main_layout.setContentsMargins(0, 0, 0, 0)

            # Создаем таблицу
            self.table_widget = QTableWidget(11, 2)
            self.table_widget.setHorizontalHeaderLabels(["Поле", "Значение"])

            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            self.table_widget.setStyleSheet("""
                QTableWidget {
                    font-size: 12px;
                    color: #000000;
                    gridline-color: #d3d3d3;
                    background-color: white;
                }
                QHeaderView::section {
                    background-color: white;
                    color:#D53032;
                    padding: 5px;
                    border: 1px solid #d3d3d3;
                    border-top:none;
                    font-size: 12px;
                    font-weight: bold;
                }
                QTableWidget QTableCornerButton::section {
                    background-color: white;
                }
                QTableWidget::item {
                    padding: 5px;
                }
            """)

            # Заполняем таблицу данными
            data = [
                ("Номер сканирования", str(self.user_details[0])),
                ("Имя", str(self.user_details[1])),
                ("Фамилия", str(self.user_details[2])),
                ("Дата Рождения", str(self.user_details[3])),
                ("Общительность (в баллах)", str(self.user_details[4])),
                ("Грамотность (в баллах)", str(self.user_details[5])),
                ("Активность (в баллах)", str(self.user_details[6])),
                ("Вовлеченность (в баллах)", str(self.user_details[7])),
                ("Степень дивации (в баллах)", str(self.user_details[8])),
                ("Результат", str(self.user_details[9])),
                ("Ссылка на профиль", str(self.user_details[10])),
            ]

            for row, (field, value) in enumerate(data):
                field_item = QTableWidgetItem(field)
                field_item.setFlags(
                    Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Запрет редактирования первого столбца
                self.table_widget.setItem(row, 0, field_item)

                value_item = QTableWidgetItem(value)
                value_item.setFlags(
                    Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)  # Запрет редактирования второго столбца
                self.table_widget.setItem(row, 1, value_item)

            # Добавляем таблицу в основной макет
            main_layout.addWidget(self.table_widget)

    def open_link(self):
        import webbrowser
        webbrowser.open(str(self.user_details[10]))