import tkinter as tk
import re
import requests
from tkinter import scrolledtext, messagebox

import users
from GetInfoFromVK import get_info
from GetToken import get_token
import testLusher as tL
from Authorization import user_authorization

SERVICE_TOKEN = get_token()
USER_TOKEN = ''

def analyze():
    input_text = text_input.get("1.0", tk.END).strip()
    input_text = extract_identifier(input_text)
    input_text = get_numeric_id(input_text, SERVICE_TOKEN)
    result = get_info(input_text, SERVICE_TOKEN, USER_TOKEN)
    # базовая инфа
    resultMainInfoUser = users.GetBase(input_text)
    result.append(resultMainInfoUser)
    # базовая инфа
    # Тест Люшера
    resultTestLusher = tL.startTestLusher(input_text)
    result.append(resultTestLusher)
    # Тест Люшера


    text_output.config(state='normal')
    text_output.delete("1.0", tk.END)
    for text in result:
        text_output.insert(tk.END, text + "\n")
    text_output.config(state='disabled')


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
    USER_TOKEN = user_authorization()
    if USER_TOKEN == '':
        messagebox.showerror("Ошибка", "Не удалось авторизоваться")
        return
    authorize_button.pack_forget()
    title_label.config(text="Введите ссылку на профиль")
    label_input.pack(pady=10)
    text_input.pack(padx=10)
    button.pack(pady=10)
    label_output.pack(pady=10)
    text_output.pack(padx=10)


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
button = tk.Button(root, text="Выполнить анализ", command=analyze)
label_output = tk.Label(root, text="Результат анализа:")
text_output = scrolledtext.ScrolledText(root, width=60, height=10, state='disabled')

root.mainloop()
