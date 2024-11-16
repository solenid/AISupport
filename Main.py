import re
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QCheckBox, QPushButton, \
    QGridLayout, QDialog, QLineEdit, QTextEdit, QComboBox, QMessageBox
from PyQt6.QtGui import QIcon
from Authorization import *  # Убедитесь, что этот импорт корректен
#Для асинхронности
import threading
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
# flagError = 0
serviceToken = getToken()

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
    def __init__(self, userID, InputTypeProf):  # Исправил метод на __init__
        super().__init__()  # Исправил вызов супер-класса
        self.setWindowTitle('HR SOLUTION')
        self.resize(1000, 600)  # Установите размер окна здесь
        self.setStyleSheet("""
            background-color: #ffffff;
        """)
        self.userID = userID
        self.typeProf = InputTypeProf
        print(f"userID => {self.userID}")
        print(f"typeProf => {self.typeProf}")

        self.layout = QGridLayout(self)  # Используйте self вместо window
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.buttons = []


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
        self.layout.addWidget(self.buttonCommonInfo, 0, 0)
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
        self.layout.addWidget(self.buttonRedFlag, 0, 1)
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
        self.layout.addWidget(self.buttonGreenFlag, 0, 2)
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
        self.layout.addWidget(self.buttonTestLusher, 0, 3)
        self.buttons.append(self.buttonTestLusher)

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
        self.layout.addWidget(self.buttonRecommendAI, 1, 0, 2, 4)
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

        self.output = QTextEdit()
        self.output.setReadOnly(True)  # Делаем поле только для чтения
        self.output.setStyleSheet("""
            margin:30px 30px 60px 30px;
            background-color:#ffffff;
            color:#000000;
            border: 2px solid #D53032; /* Граница кнопки */
        """)
        self.layout.addWidget(self.output, 3, 0, 5, 5)
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
            border-top: none;
            border-right: none;
            border-left: none; 
            border-radius: 1px; /* Скругление углов */
            cursor: pointer;
        """)
        self.layout.addWidget(self.buttonHistory, 4, 0)
        self.buttons.append(self.buttonHistory)
        self.buttonHistory.clicked.connect(self.clickHistory)

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

    def clickHistory(self):
        print("History")
        show_history()

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
        self.button.setEnabled(True)
    def onTap(self):
        # self.button.setEnabled(False)
        t1 = threading.Thread(target=self.runAsyncTasks, daemon=True)
        t1.start()

    def update_output(self, result):
        for i in result[0]:
            dataForCommonInfo.append(i)
        for i in result[1]:
            dataForRedFlag.append(i)
        for i in result[2]:
            dataForGreenFlag.append(i)
        for i in result[3]:
            dataForRecommend.append(i)
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




class OptionsPage(QWidget):  # Исправил название класса на optionsPage
    def __init__(self):  # Исправил метод на __init__
        super().__init__()  # Исправил вызов супер-класса
        self.setWindowTitle('HR SOLUTION')
        self.resize(800, 600)  # Установите размер окна здесь
        self.setStyleSheet("""
            background-color: #ffffff;
        """)

        self.layout = QGridLayout(self)  # Используйте self вместо window
        self.layout.setContentsMargins(25, 0, 25, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.combobox = QComboBox()
        # self.icon_people_nature = QIcon('people-animal2.png')
        # self.icon_people_people = QIcon('people-people.png')
        # self.icon_people_symbol = QIcon('people-symbol.png')
        # self.icon_people_tech = QIcon('people-tech.png')
        # self.icon_people_art = QIcon('people-art.png')

        # Словарь с данными
        self.data_dict = {
            'Error': "Произошла ошибка"
        }
        self.typeProf = 10
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

            # Подключаем сигнал изменения текущего индекса к слоту
        self.combobox.currentIndexChanged.connect(self.on_combobox_changed)
        self.layout.addWidget(self.combobox, 0, 0)


        self.combobox.setStyleSheet("""
            font-size: 22px;
            background-color: #ffffff;
            color: #000000;
            font-weight: bold;
            padding: 5px 0px 5px 10px; /* Отступы внутри кнопки */
            border: 0.5px solid #D53032; /* Граница кнопки */
            border-radius: 5px; /* Скругление углов */
        """)

        self.inputText = QLineEdit()
        self.inputText.setStyleSheet("""
            font-size: 22px;
            background-color: #ffffff;
            color: #000000;
            font-weight: bold;
            border: 0.5px solid #D53032; /* Граница кнопки */
            border-radius: 5px; /* Скругление углов */
        """)
        self.layout.addWidget(self.inputText, 2, 0)
        self.label = QLabel("вставьте ссылку кандидата")
        self.label.setStyleSheet("""
            font-size: 18px;
            background-color: #ffffff;
            color: #000000;
        """)
        self.layout.addWidget(self.label, 1, 0)

        self.button = QPushButton("Начать анализ")
        self.button.setStyleSheet("""
                    background-color: #D53032;
                    color: #ffffff;
                    font-size:24px;
                    font-style: italic;
                    margin:10px 0px 0px 0px;
                    padding: 1px 50px 1px 50px; /* Отступы внутри кнопки */
                    border: 0.5px solid #D53032; /* Граница кнопки */
                    border-radius: 5px; /* Скругление углов */
                """)
        self.layout.addWidget(self.button, 3, 0)
        self.button.clicked.connect(self.show_TestPage)

    def show_TestPage(self):
        InputUserId = self.inputText.text().strip()
        InputTypeProf = int(self.typeProf)
        if InputTypeProf == 10:
            self.showInfoMessage("Вы не выбрали профессию!")
        else:
            self.TestPage = TestPage(InputUserId, InputTypeProf)
            self.TestPage.show()
            self.close()  # Закрываем текущее окно

    def on_combobox_changed(self, index):
        # Получаем ключ выбранного элемента
        self.typeProf = self.combobox.itemData(index)  # Это ключ из словаря
        value = self.combobox.currentText()   # Это отображаемое значение
        print(f'Выбранный элемент: {value}, Ключ: {self.typeProf}')

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Произошла ошибка!")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        # Показать сообщение и дождаться закрытия
        msg_box.exec()

        # Закрыть главное окно после закрытия QMessageBox
        self.close()

    def showInfoMessage(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText("Инфо!")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Информация")
        # Показать сообщение и дождаться закрытия
        msg_box.exec()

        # Закрыть главное окно после закрытия QMessageBox
        self.close()




if __name__ == '__main__':  # Исправил на __name__ == '__main__'
    app = QApplication([])
    testP = authPage()  # Исправил на TestPage
    testP.setStyleSheet(
        "background-color: #ffffff; "
    )
    testP.resize(800, 600)
    testP.show()

    # testP2 = TestPage()
    # testP2.setStyleSheet(
    #     "background-color: #ffffff; "
    # )
    # testP2.resize(800, 600)
    # testP2.show()


    # testP3 = OptionsPage()  # Исправил на TestPage
    # testP3.setStyleSheet(
    #     "background-color: #ffffff; "
    # )
    # testP3.resize(800, 600)
    # testP3.show()

    exit(app.exec())
