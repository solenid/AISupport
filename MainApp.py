import tkinter as tk
import re
import requests
from tkinter import scrolledtext
from GetInfoFromVK import get_info
from GetToken import get_token

TOKEN = get_token()


def analyze():
    input_text = text_input.get("1.0", tk.END).strip()
    input_text = extract_identifier(input_text)
    input_text = get_numeric_id(input_text, TOKEN)
    result = get_info(input_text)
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


root = tk.Tk()
root.title("AI_HELPER")
root.geometry("800x600")

label_input = tk.Label(root, text="Введите id:")
label_input.pack(pady=10)

text_input = scrolledtext.ScrolledText(root, width=60, height=10)
text_input.pack(padx=10)

button = tk.Button(root, text="Выполнить анализ", command=analyze)
button.pack(pady=10)

label_output = tk.Label(root, text="Результат анализа:")
label_output.pack(pady=10)

text_output = scrolledtext.ScrolledText(root, width=60, height=10, state='disabled')
text_output.pack(padx=10)

root.mainloop()
