import tkinter as tk
import re
import requests
from tkinter import scrolledtext, messagebox

from GetInfoFromVK import getInfoFromVK
from GetToken import getToken
import TestLusher as tL
from Authorization import userAuthorization
#Для асинхронности
import threading
import asyncio

serviceToken = getToken()
userToken = ''

#Эти функции принимают id и функцию вывода в табличку
# и свой результат сразу кидают в функцию из аргументов
#----------------------------------------------------------------------------------
#Функция для запуска Анализа
async def analyze(IDuser, updateOutput1):
    updateOutput1 (getInfoFromVK(IDuser, serviceToken, userToken))

#Функция для запуска теста Люшера
async def lysher(IDuser, updateOutput2):
    updateOutput2(tL.startTestLusher(IDuser))
# ----------------------------------------------------------------------------------

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

def onAuthorize():
    global userToken
    userToken = userAuthorization()
    if userToken == '':
        messagebox.showerror("Ошибка", "Не удалось авторизоваться")
        return
    authorizeButton.pack_forget()
    titleLabel.config(text="Введите ссылку на профиль")
    labelInput.pack(pady=10)
    textInput.pack(padx=10)
    button.pack(pady=10)
    labelOutput.pack(pady=10, side='left')
    labelOutput2.pack(pady=10, side='right')
    textOutput.pack(pady=15, side='left')
    textOutput2.pack(pady=15, side='right')


#Вычисляет id пользовтеля и тут же начинает бесконечный цикл ожидания завершения функций
#Вероятно нужно придумать как блокировать кнопку при едином ее нажатии
#Потому что никак не противоречит что у нас много функций в многих потоках, но вывод то у них 1, и они будут его перезаписывать
def runAsyncTasks(updateOutput1, updateOutput2):
    userID = textInput.get("1.0", tk.END).strip()
    userID = extractIdentifier(userID)
    userID = getNumericID(userID, serviceToken)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(
        analyze(userID, updateOutput1),
        lysher(userID, updateOutput2),
    ))

#Вероятно нужно придумать как блокировать кнопку при едином ее нажатии
def onTap():
    threading.Thread(target=runAsyncTasks, args=(OutputMany, OutputSolo)).start()

#Функция которая пишет в таблицу (Много аргументов)
def OutputMany(result):
    textOutput.config(state='normal')
    textOutput.delete("1.0", tk.END)
    for text in result:
        textOutput.insert(tk.END, text + "\n")
    textOutput.config(state='disabled')

#Функция которая пишет в таблицу (Один Аргумент)
def OutputSolo(result):
    textOutput2.config(state='normal')
    textOutput2.delete("1.0", tk.END)
    textOutput2.insert(tk.END, result)
    textOutput2.config(state='disabled')

root = tk.Tk()
root.title("AI_HELPER")
root.geometry("800x600")
root.title("Авторизация через VK ID")

titleLabel = tk.Label(root, text="АВТОРИЗУЙТЕСЬ В СЕРВИСЕ С ПОМОЩЬЮ VK ID", font=("Arial", 14))
titleLabel.pack(pady=10)

authorizeButton = tk.Button(root, text="Авторизоваться", command=onAuthorize)
authorizeButton.pack(pady=5)

labelInput = tk.Label(root, text="Введите id:")
textInput = scrolledtext.ScrolledText(root, width=60, height=10)
button = tk.Button(root, text="Выполнить анализ", command=onTap)
labelOutput = tk.Label(root, text="Результат анализа:")
labelOutput2 = tk.Label(root, text="Результат Люшера:")
textOutput = scrolledtext.ScrolledText(root, width=35, wrap = tk.WORD, height=10, state='disabled')
textOutput2 = scrolledtext.ScrolledText(root, width=35, wrap = tk.WORD, height=10, state='disabled')
root.mainloop()
