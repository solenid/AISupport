import tkinter as tk
import re
import requests
from tkinter import scrolledtext, messagebox, font, ttk

import requests
import TestLusher as tL
from GetInfoFromVK import *
from GetToken import getToken
from Authorization import userAuthorization
from HistoryWindow import *
import threading
import asyncio
import re

serviceToken = getToken()
userToken = ''

async def analyze(IDuser, updateOutput1):
    updateOutput1(getInfoFromVK(IDuser, serviceToken, userToken))


async def lysher(IDuser, updateOutput2):
    updateOutput2(tL.startTestLusher(IDuser))


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
    # print(data)
    return str(data['response'][0]['id'])


def onAuthorize():
    global userToken
    if userToken != '':
        buttonAnalyze.pack(anchor='nw')
        buttonHistory.pack(anchor='nw')
        authorizeButton.pack_forget()
        titleLabel.config(text="Введите ссылку на профиль")
        labelInput.pack(pady=10)
        textInput.pack(padx=10)
        button.pack(pady=10)
        labelOutput.pack(pady=10, side='left')
        labelOutput2.pack(pady=10, side='right')
        textOutput.pack(pady=15, side='left')
        textOutput2.pack(pady=15, side='right')
    else:
        userToken = userAuthorization()
        if userToken == '':
            messagebox.showerror("Ошибка", "Не удалось авторизоваться")
            return
        onAuthorize()



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
    button.config(state=tk.ACTIVE)


def onTap():
    button.config(state=tk.DISABLED)
    t1 = threading.Thread(target=runAsyncTasks, args=(OutputMany, OutputSolo), daemon=True)
    t1.start()


def OutputMany(result):
    textOutput.config(state='normal')
    textOutput.delete("1.0", tk.END)
    for text in result:
        textOutput.insert(tk.END, text + "\n")
    textOutput.config(state='disabled')


def OutputSolo(result):
    textOutput2.config(state='normal')
    textOutput2.delete("1.0", tk.END)
    textOutput2.insert(tk.END, result)
    textOutput2.config(state='disabled')


root = tk.Tk()
root.configure(bg='White')
tkStyle = ttk.Style()
fontAuthLabel = font.Font(family= "Arial Rounded MT Bold", size=18, weight="normal", slant="roman", underline=False, overstrike=False)
fontAuthButton = font.Font(family= "Arial Rounded MT Bold", size=18, weight="normal", slant="italic", underline=False, overstrike=False)
tkStyle.configure("TLabel",  font=fontAuthLabel, foreground="#FF0000", padding=8, background="#ffffff")
root.title("AI_HELPER")
root.geometry("800x600")
root.title("Авторизация через VK ID")
titleLabel = ttk.Label(root, text="Войдите в систему", style="TLabel")
titleLabel.pack(pady=10)

authorizeButton = tk.Button(root,font=fontAuthButton, text="VK ID", bg="White", borderwidth=1,fg = "red", relief="ridge", command=onAuthorize)
authorizeButton.pack(pady=5)

labelInput = tk.Label(root, text="Введите id:")
textInput = scrolledtext.ScrolledText(root, width=60, height=10)
button = tk.Button(root, text="Выполнить анализ", command=onTap)
buttonAnalyze = tk.Button(root, text="Анализ", width=6, height=1, command=onAuthorize)
buttonHistory = tk.Button(root, text="История", width=6, height=1, command=lambda: show_history(root))
labelOutput = tk.Label(root, text="Результат анализа:")
labelOutput2 = tk.Label(root, text="Результат Люшера:")
textOutput = scrolledtext.ScrolledText(root, width=35, wrap=tk.WORD, height=10, state='disabled')
textOutput2 = scrolledtext.ScrolledText(root, width=35, wrap=tk.WORD, height=10, state='disabled')
root.mainloop()
