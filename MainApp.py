import tkinter as tk
import re
import requests
from tkinter import scrolledtext, messagebox

from GetInfoFromVK import getInfoFromVK
from GetToken import get_token
import TestLusher as tL
from Authorization import userAuthorization
#Для асинхронности
import threading
import asyncio

SERVICE_TOKEN = get_token()
USER_TOKEN = ''

#Эти функции принимают id и функцию вывода в табличку
# и свой результат сразу кидают в функцию из аргументов
#----------------------------------------------------------------------------------
#Функция для запуска Анализа
async def analyze(id_user, updateOutput1):
    updateOutput1 (getInfoFromVK(id_user, SERVICE_TOKEN, USER_TOKEN))

#Функция для запуска теста Люшера
async def lysher(id_user, updateOutput2):
    updateOutput2(tL.startTestLusher(id_user))
# ----------------------------------------------------------------------------------

def extract_identifier(vk_url):
    pattern = r'https?://(?:www\.)?vk\.com/([^/?#&]+)'
    match = re.match(pattern, vk_url)
    if match:
        return match.group(1)
    else:
        return None


def get_numeric_id(user_identifier, access_token, api_version='5.131'):
    url = 'https://api.vk.com/method/users.get'
    params = {'user_ids': user_identifier,
              'access_token': access_token,
              'v': api_version}
    response = requests.get(url, params=params)
    data = response.json()
    return str(data['response'][0]['id'])

def on_authorize():
    global USER_TOKEN
    USER_TOKEN = userAuthorization()
    if USER_TOKEN == '':
        messagebox.showerror("Ошибка", "Не удалось авторизоваться")
        return
    authorize_button.pack_forget()
    title_label.config(text="Введите ссылку на профиль")
    label_input.pack(pady=10)
    text_input.pack(padx=10)
    button.pack(pady=10)
    label_output.pack(pady=10,side='left')
    label_output2.pack(pady=10, side='right')
    text_output.pack(pady=15, side='left')
    text_output2.pack(pady=15, side='right')


#Вычисляет id пользовтеля и тут же начинает бесконечный цикл ожидания завершения функций
#Вероятно нужно придумать как блокировать кнопку при едином ее нажатии
#Потому что никак не противоречит что у нас много функций в многих потоках, но вывод то у них 1, и они будут его перезаписывать
def runAsyncTasks(updateOutput1, updateOutput2):
    id_user = text_input.get("1.0", tk.END).strip()
    id_user = extract_identifier(id_user)
    id_user = get_numeric_id(id_user, SERVICE_TOKEN)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(
        analyze(id_user, updateOutput1),
        lysher(id_user, updateOutput2),
    ))

#Вероятно нужно придумать как блокировать кнопку при едином ее нажатии
def onTap():
    threading.Thread(target=runAsyncTasks, args=(OutputMany, OutputSolo)).start()

#Функция которая пишет в таблицу (Много аргументов)
def OutputMany(result):
    text_output.config(state='normal')
    text_output.delete("1.0", tk.END)
    for text in result:
        text_output.insert(tk.END, text + "\n")
    text_output.config(state='disabled')

#Функция которая пишет в таблицу (Один Аргумент)
def OutputSolo(result):
    text_output2.config(state='normal')
    text_output2.delete("1.0", tk.END)
    text_output2.insert(tk.END, result)
    text_output2.config(state='disabled')

root = tk.Tk()
root.title("AI_HELPER")
root.geometry("800x600")
root.title("Авторизация через VK ID")

title_label = tk.Label(root, text="АВТОРИЗУЙТЕСЬ В СЕРВИСЕ С ПОМОЩЬЮ VK ID", font=("Arial", 14))
title_label.pack(pady=10)

authorize_button = tk.Button(root, text="Авторизоваться", command=on_authorize)
authorize_button.pack(pady=5)

label_input = tk.Label(root, text="Введите id:")
text_input = scrolledtext.ScrolledText(root, width=60, height=10)
button = tk.Button(root, text="Выполнить анализ", command=onTap)
label_output = tk.Label(root, text="Результат анализа:")
label_output2 = tk.Label(root, text="Результат Люшера:")
text_output = scrolledtext.ScrolledText(root, width=35, wrap = tk.WORD, height=10, state='disabled')
text_output2 = scrolledtext.ScrolledText(root, width=35, wrap = tk.WORD, height=10, state='disabled')
root.mainloop()
