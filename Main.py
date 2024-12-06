import re
import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QCheckBox, QPushButton, \
    QGridLayout, QDialog, QLineEdit, QTextEdit, QComboBox, QMessageBox, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QIcon

from Authorization import *  # Убедитесь, что этот импорт корректен
# Для асинхронности
import threading
import json
import asyncio
import TestLusher as tL
from HistoryWindow import *
from GetInfoFromVK import getInfoFromVK
from GetToken import getToken

dataForCommonInfo = [""]
dataForRedFlag = [""]
dataForGreenFlag = [""]
dataForRecommend = [""]
dataForTestLusher = [""]
dataForTestGerchikov = [""]
serviceToken = getToken()
statusLoad = 0


def extractIdentifier(vkURL):
    pattern = r'https?://(?:www\.)?vk\.com/([^/?#&]+)'
    match = re.match(pattern, vkURL)
    if match:
        return match.group(1)
    else:
        return None


def getNumericID(userIdentifier, accessToken, apiVersion='5.131'):
    url = 'https://api.vk.com/method/users.get'
    params = {'user_ids': userIdentifier,
              'access_token': accessToken,
              'v': apiVersion}
    response = requests.get(url, params=params)
    data = response.json()
    return str(data['response'][0]['id'])


class authPage(QWidget):  # Исправил название класса на TestPage
    def __init__(self):  # Исправил метод на __init__
        super().__init__()  # Исправил вызов супер-класса
        self.setWindowTitle('HR SOLUTION')
        self.resize(800, 600)  # Установите размер окна здесь
        self.setStyleSheet("""
            background-color: #ffffff;
        """)

        self.layout = QGridLayout(self)  # Используйте self вместо window
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Войдите в систему")
        self.label.setStyleSheet("""
            font-size: 24px;
            background-color: #ffffff;
            color: #D53032;
            font-weight: bold;
            padding: 0% 0% 00% 40%; /* Отступы внутри кнопки */
            text-align: center;
        """)
        self.layout.addWidget(self.label, 0, 0)

        self.button = QPushButton("VK ID")
        self.button.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            font-style: italic;
            margin:5px 0px 0px 0px;
            padding: 5px 250px 5px 10px; /* Отступы внутри кнопки */
            border: 0.5px solid #D53032; /* Граница кнопки */
            border-radius: 5px; /* Скругление углов */
        """)
        self.layout.addWidget(self.button, 1, 0)

        self.button.clicked.connect(self.authorization)

    def show_optionsPage(self):
        self.optionsPage = OptionsPage()
        self.optionsPage.show()
        self.close()  # Закрываем текущее окно

    def authorization(self):
        global userToken
        userToken = userAuthorization()  # Убедитесь, что эта функция определена
        myDi = QDialog(self)
        if userToken == '':
            myDi.setWindowTitle("Ошибка")
            myDi.setModal(True)
            myDi.exec()  # Показываем диалог
            return
        print(userToken)
        self.show_optionsPage()


class TestPage(QWidget):  # Исправил название класса на TestPage
    def __init__(self, userID, InputTypeProf, prof):  # Исправил метод на __init__
        super().__init__()  # Исправил вызов супер-класса
        self.setWindowTitle('HR SOLUTION')
        self.resize(1000, 600)  # Установите размер окна здесь
        self.setStyleSheet("""
            background-color: #ffffff;
        """)
        self.userID = userID
        self.typeProf = InputTypeProf
        self.prof = prof
        print(f"userID => {self.userID}")
        print(f"typeProf => {self.typeProf}")
        print(f"prof => {self.prof}")

        self.layout = QGridLayout(self)  # Используйте self вместо window
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.buttons = []

        self.labelWindow = QLabel("ХАРАКТЕРИСТИКА СОИСКАТЕЛЯ")
        # Label для окна
        self.labelWindow.setStyleSheet("""
            font-size: 24px;
            font-weight:bold;
            margin:0px 0px 50px 0px;
            color: #D53032;
        """)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрирование текста
        self.layout.addWidget(self.labelWindow, 0, 2)

        self.labelProf = QLabel(f"Профессия - {self.prof}")
        # Label для окна
        self.labelProf.setStyleSheet("""
            font-size: 24px;
            font-weight:bold;
            margin:0px 0px 50px 0px;
            color: #D53032;
        """)
        self.labelProf.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрирование текста
        self.layout.addWidget(self.labelProf, 1, 2)

        self.buttonCommonInfo = QPushButton("Общая информация")
        self.buttonCommonInfo.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:30px 0px 0px 0px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */
            border-top: none;
            border-right: none;
            border-left: none; 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonCommonInfo, 2, 0)
        self.buttons.append(self.buttonCommonInfo)

        self.buttonRedFlag = QPushButton("RED FLAGs")
        self.buttonRedFlag.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:30px 0px 0px 15px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */
            border-top: none;
            border-right: none;
            border-left: none; 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonRedFlag, 2, 1)
        self.buttons.append(self.buttonRedFlag)

        self.buttonGreenFlag = QPushButton("GREEN FLAGs")
        self.buttonGreenFlag.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:30px 0px 0px 15px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */
            border-top: none;
            border-right: none;
            border-left: none; 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonGreenFlag, 2, 2)
        self.buttons.append(self.buttonGreenFlag)

        self.buttonTestLusher = QPushButton("ТЕСТ ЛЮШЕРА")
        self.buttonTestLusher.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:30px 0px 0px 15px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */
            border-top: none;
            border-right: none;
            border-left: none; 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonTestLusher, 2, 3)
        self.buttons.append(self.buttonTestLusher)

        self.buttonTestGerchikova = QPushButton("ТЕСТ ГЕРЧИКОВА")
        self.buttonTestGerchikova.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:30px 0px 0px 15px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */
            border-top: none;
            border-right: none;
            border-left: none; 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonTestGerchikova, 2, 4)
        self.buttons.append(self.buttonTestGerchikova)

        self.buttonRecommendAI = QPushButton("Рекомендации AI")
        self.buttonRecommendAI.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:30px 0px 30px 0px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */
            border-top: none;
            border-right: none;
            border-left: none; 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonRecommendAI, 3, 0, 2, 5)
        self.buttons.append(self.buttonRecommendAI)

        self.layout.setColumnStretch(0, 2)  # Столбец 0
        self.layout.setColumnStretch(1, 1)  # Столбец 1
        self.layout.setColumnStretch(2, 1)  # Столбец 2
        self.layout.setColumnStretch(3, 1)  # Столбец 3

        self.buttonCommonInfo.clicked.connect(self.clickButtonCommonInfo)
        self.buttonRedFlag.clicked.connect(self.clickButtonRedFlag)
        self.buttonGreenFlag.clicked.connect(self.clickButtonGreenFlag)
        self.buttonTestLusher.clicked.connect(self.clickButtonTestLusher)
        self.buttonRecommendAI.clicked.connect(self.clickButtonRecommend)
        self.buttonTestGerchikova.clicked.connect(self.clickButtonGerchikov)

        self.output = QTextEdit()
        self.output.setReadOnly(True)  # Делаем поле только для чтения
        self.output.setStyleSheet("""
            margin:30px 30px 60px 30px;
            background-color:#ffffff;
            color:#000000;
            border: 2px solid #D53032; /* Граница кнопки */
        """)
        self.layout.addWidget(self.output, 4, 0, 5, 5)
        self.output.hide()  # Скрываем текстовое поле

        self.buttonHistory = QPushButton("История")
        self.buttonHistory.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:300% 0px 0px 0px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */ 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonHistory, 5, 4)
        self.buttons.append(self.buttonHistory)
        self.buttonHistory.clicked.connect(self.clickHistory)

        self.buttonGoBack = QPushButton("<= Назад")
        self.buttonGoBack.setStyleSheet("""
            background-color: #ffffff;
            color: #D53032;
            font-size:18px;
            margin:300% 0px 0px 0px;
            font-weight: bold;
            padding: 1px 10px 1px 10px; /* Отступы внутри кнопки */
            border: 2px solid #D53032; /* Граница кнопки */
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonGoBack, 5, 0)
        self.buttons.append(self.buttonGoBack)
        self.buttonGoBack.clicked.connect(self.clickGoBack)

    def clickButtonCommonInfo(self):
        if not self.output.isHidden():
            self.output.hide()  # Скрываем текстовое поле
        self.output.clear()
        for i in dataForCommonInfo:
            self.output.append(i)
        self.output.show()  # Скрываем текстовое поле

    def clickButtonRedFlag(self):
        if not self.output.isHidden():
            self.output.hide()  # Скрываем текстовое поле
        self.output.clear()
        for i in dataForRedFlag:
            self.output.append(i)
        self.output.show()  # Скрываем текстовое поле

    def clickButtonGreenFlag(self):
        if not self.output.isHidden():
            self.output.hide()  # Скрываем текстовое поле
        self.output.clear()
        for i in dataForGreenFlag:
            self.output.append(i)
        self.output.show()  # Скрываем текстовое поле

    def clickButtonTestLusher(self):
        if not self.output.isHidden():
            self.output.hide()  # Скрываем текстовое поле
        self.output.clear()
        for i in dataForTestLusher:
            self.output.append(i)
        self.output.show()  # Скрываем текстовое поле

    def clickButtonRecommend(self):
        if not self.output.isHidden():
            self.output.hide()  # Скрываем текстовое поле
        self.output.clear()
        for i in dataForRecommend:
            self.output.append(i)
        self.output.show()  # Скрываем текстовое поле

    def clickButtonGerchikov(self):
        if not self.output.isHidden():
            self.output.hide()  # Скрываем текстовое поле
        self.output.clear()
        for i in dataForTestGerchikov:
            self.output.append(i)
        self.output.show()  # Скрываем текстовое поле

    def clickHistory(self):
        self.HistoryWindow = HistoryWindow()
        self.HistoryWindow.show()
        # self.close()  # Закрываем текущее окно

    def clickGoBack(self):
        self.OptionsPage = OptionsPage()
        self.OptionsPage.show()
        self.close()

    def runAsyncTasks(self):
        # userID = self.inputText.text().strip()
        self.userID = extractIdentifier(self.userID)
        self.userID = getNumericID(self.userID, serviceToken)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.gather(
            self.analyze(self.userID),
            self.lysher(self.userID),
        ))

    def loadingData(self):
        self.indexElem = 0
        # current_text = self.button.text()
        while statusLoad != 1:
            statusButton = ['Общая информация','Общая информация.','Общая информация..', 'Общая информация...']
            new_text = statusButton[self.indexElem]
            if self.indexElem == 3:
                self.indexElem = 0
            else:
                self.indexElem+=1

            # self.buttonCommonInfo.setText(new_text)
            # QTimer.singleShot(1000,self.buttonCommonInfo.setText(new_text))

    def onTap(self):
        self.t1 = threading.Thread(target=self.runAsyncTasks, daemon=True)
        self.t1.start()
        # t2 = threading.Thread(target=self.loadingData, daemon=True)
        # t2.start()

    def update_output(self, result):
        for i in result[0]:
            dataForCommonInfo.append(i)
        for i in result[1]:
            dataForRedFlag.append(i)
        for i in result[2]:
            dataForGreenFlag.append(i)
        for i in result[3]:
            dataForRecommend.append(i)
        for i in result[4]:
            dataForTestGerchikov.append(i)

    def update_output2(self, result):
        dataForTestLusher.append(result)

    # Функция для запуска Анализа
    async def analyze(self, IDuser):
        self.update_output(getInfoFromVK(IDuser, serviceToken, userToken, self.typeProf))

    # Функция для запуска теста Люшера
    async def lysher(self, IDuser):
        self.update_output2(tL.startTestLusher(IDuser))

    def showEvent(self, event):
        super().showEvent(event)  # Вызов метода родителя
        self.onTap()  # Вызов вашей функции


class OptionsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.help_window = None
        self.typeProf = 10
        self.selected_textProf = "None"

        self.setWindowTitle('HR SOLUTION')
        self.resize(800, 600)  # Установите размер окна здесь
        self.setStyleSheet("""
            background-color: #ffffff;
            """)

        # Создаем грид-лэйаут
        layout = QGridLayout()
        layout.setContentsMargins(25, 0, 25, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Объявление
        self.combobox = QComboBox()
        self.inputText = QLineEdit()
        self.button = QPushButton("Перейти к анализу =>")
        self.buttonHelp = QPushButton("Узнать подробнее про типы")
        # Создаем QLabel для отображения выбранного элемента
        self.label = QLabel('Выберите элемент из списка')
        self.labelWindow = QLabel('Отбор соискателей')

        # СТИЛИ
        # СПИСОК
        self.combobox.setStyleSheet("""
            font-size: 20px;
            background-color: #ffffff;
            color: #000000;
            font-weight: bold;
            padding: 5px 0px 5px 0px; /* Отступы внутри кнопки */
            border: 0.5px solid #D53032; /* Граница кнопки */
            border-radius: 5px; /* Скругление углов */
        """)

        # Поле ввода
        self.inputText.setStyleSheet("""
            font-size: 20px;
            background-color: #ffffff;
            color: #000000;
            font-weight: bold;
            border: 0.5px solid #D53032; /* Граница кнопки */
            margin:25px 0px 10px 0px;
            border-radius: 5px; /* Скругление углов */
        """)
        self.inputText.setPlaceholderText("Вставьте ссылку кандидата")

        # Кнопка
        self.button.setStyleSheet("""
                    background-color: #D53032;
                    color: #ffffff;
                    font-size:24px;
                    margin:10px 0px 0px 0px;
                    padding: 1px 50px 1px 50px; /* Отступы внутри кнопки */
                    border: 0.5px solid #D53032; /* Граница кнопки */
                    border-radius: 5px; /* Скругление углов */
                """)

        # Кнопка помощи
        self.buttonHelp.setStyleSheet("""
                color:#D53032;
                padding:0px 0px 5px 0px;
                border-bottom: 1px solid #D53032;
                font-style: italic;
                font-size:18px;
                """)

        # Поле типа
        self.label.setStyleSheet("""
            font-size: 20px;
            background-color: #D53032;
            color: #ffffff;
            padding: 5px;
            font-weight: bold;
            border: 0.5px solid #ffffff; /* Граница кнопки */
            margin: 0px 0px 0px 10px;
            border-radius: 5px; /* Скругление углов */
        """)

        # Label для окна
        self.labelWindow.setStyleSheet("""
            font-size: 24px;
            font-weight:bold;
            margin:0px 0px 50px 0px;
            color: #D53032;
        """)
        self.labelWindow.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрирование текста

        # СТИЛИ

        self.data_dict = {
            'Error': "Произошла ошибка"
        }
        self.flagError = 0
        try:
            with open('prof.json', 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.flagError = 1
            self.show_error_message("Ошибка: Файл не найден. Убедитесь, что файл 'prof.json' существует.")
        except json.JSONDecodeError:
            self.flagError = 1
            self.show_error_message("Ошибка: Не удалось декодировать JSON. Проверьте правильность формата файла.")
        except Exception as e:
            self.flagError = 1
            self.show_error_message(f"Произошла ошибка: {e}")

        if not self.flagError:
            # Добавляем элементы в комбобокс
            for key, values in self.data.items():
                for value in values:
                    self.combobox.addItem(value, key)
        else:
            self.combobox.addItem(self.data_dict['Error'])

        # Подключаем сигнал изменения текста к слоту
        self.combobox.currentIndexChanged.connect(self.update_label)

        # Подключаем сигнал перехода на следующую страницу
        self.button.clicked.connect(self.show_TestPage)

        # Подключаем сигнал показа страницы помощи
        self.buttonHelp.clicked.connect(self.showHelpWindow)

        # Добавление виджетов в layout
        layout.addWidget(self.combobox, 1, 0)  # Добавляем ComboBox в строку 0, столбец 0
        layout.addWidget(self.label, 1, 1)   # Добавляем QLabel в строку 0, столбец 1
        layout.addWidget(self.labelWindow, 0 , 0, 1 , 2)
        layout.addWidget(self.inputText, 4, 0, 1, 4)
        layout.addWidget(self.buttonHelp, 3, 1)
        layout.addWidget(self.button, 5, 1)

        # Устанавливаем layout для главного окна
        self.setLayout(layout)


    def show_TestPage(self):
        InputUserId = self.inputText.text().strip()
        InputTypeProf = int(self.typeProf)
        if InputTypeProf == 10:
            self.showInfoMessage("Вы не выбрали профессию!")
        else:
            self.TestPage = TestPage(InputUserId, InputTypeProf, self.selected_textProf)
            self.TestPage.show()
            self.close()  # Закрываем текущее окно

    def showHelpWindow(self):
        if self.help_window is None:  # Создаем новое окно только если оно еще не создано
            self.help_window = HelpWindow()
        self.help_window.show()

    def show_error_message(self, message):
        msg_box = QMessageBox()
        # msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Произошла ошибка!")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        # Показать сообщение и дождаться закрытия
        msg_box.exec()

        # Закрыть главное окно после закрытия QMessageBox
        self.close()

    def showInfoMessage(self, message):
        msg_box = QMessageBox()
        # msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Инфо!")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Информация")
        # Показать сообщение и дождаться закрытия
        msg_box.exec()

        # Закрыть главное окно после закрытия QMessageBox
        self.close()

    def update_label(self, index):
        type_dict = {
            -1: 'Выбранный тип: Человек-человек',
            0: 'Выбранный тип: Человек-природа',
            1: 'Выбранный тип: Человек-человек',
            2: 'Выбранный тип: Человек-знак',
            3: 'Выбранный тип: Человек-техника',
            4: 'Выбранный тип: Человек-художественный образ'
        }

        selected_key = self.combobox.itemData(index)  # Ключ (userData) выбранного элемента
        self.typeProf = selected_key
        # Получаем строку из словаря по значению selected_key
        selected_text = type_dict.get(int(selected_key), 'Выберите элемент из списка')
        self.selected_textProf = self.combobox.currentText()

        # Обновляем метку с выбранным текстом
        self.label.setText(f"Выбранный элемент: {self.selected_textProf}")

        # Устанавливаем текст метки
        self.label.setText(selected_text)

        print(f"selected_text => {selected_text}")
        print(f"selected_key => {selected_key}")
        print(f"selected_textProf => {self.selected_textProf}")



class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.setStyleSheet("background-color:#ffffff;")

        # Создаем виджеты для каждого типа человека
        types = [
            ("Человек-природа", "Представители этого типа имеют дело с растительными и животными организмами, микроорганизмами и условиями их существования."),
            ("Человек-человек", "Предметом интереса, распознавания, обслуживания, преобразования здесь являются социальные системы, сообщества, группы населения, люди разного возраста."),
            ("Человек-знак", "Естественные и искусственные языки, условные знаки, символы, цифры, формулы - вот предметные миры, которые занимают представителей профессий этого типа."),
            ("Человек-техника", "Работники имеют дело с неживыми, техническими объектами труда."),
            ("Человек-художественный образ", "Явления, факты художественного отображения действительности - вот что занимает представителей этого типа профессий.")
        ]

        for type_name, description in types:
            hbox = QHBoxLayout()

            # Объявления
            # Объявление Label для каждого пункта
            label = QLabel(type_name)
            # Объявление Description для каждого пункта
            description_label = QLabel(description)

            # Стили
            label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: black;
            border-bottom: 2px solid red;
            margin:0;
            padding:0;
            """)
            label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

            # Стили для описания
            description_label.setStyleSheet("""
            font-size:14px;
            color: black;
            border-bottom: 2px solid red;
            margin:0;
            padding:0;
            """)
            description_label.setWordWrap(True)

            # Добавляем пробел между меткой и описанием
            hbox.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
            # Добавление
            hbox.addWidget(label)
            hbox.addWidget(description_label)
            layout.addLayout(hbox)


        self.setLayout(layout)
        self.setWindowTitle('Типы профессий')
        self.setGeometry(350, 150, 800, 400)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = authPage()
    window.show()
    sys.exit(app.exec())