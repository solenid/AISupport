import tkinter as tk
from tkinter import ttk, messagebox
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


def show_more_details(scan_id, root):
    user_details = getUserById(scan_id)
    if user_details:
        # Создаём новое окно
        details_window = tk.Toplevel(root)
        details_window.title("Детали пользователя")
        details_window.geometry("600x400")

        # Создаём Treeview с двумя столбцами
        tree = ttk.Treeview(details_window, columns=("field", "value"), show="headings")
        tree.heading("field", text="Поле")
        tree.heading("value", text="Значение")
        tree.column("field", width=200, anchor='w')
        tree.column("value", width=400, anchor='w')
        tree.pack(fill=tk.BOTH, expand=True)

        column_names = ["Номер сканирования", "Имя", "Фамилия", "Дата Рождения", "Количество друзей",
                        "Количество Постов", "Количество Комментариев", "Количество Лайков", "Количество матов",
                        "Количество ошибок", "Экстремисткие слова", "Слова-Угрозы", "Темы групп", "Рейтинг Пользователя", "Ссылка на пользователя"]

        # Вставляем пары поле-значение в Treeview
        for col, val in zip(column_names, user_details):
            tree.insert("", "end", values=(col, val))


def show_history():
    history_window = tk.Tk()
    history_window.title("История сканов")
    history_window.geometry("1200x600")
    history_window.configure(bg='White')


    columns = ("scan_id", "first_name", "last_name", "birth_date", "more")
    tree = ttk.Treeview(history_window, columns=columns, show="headings")

    tree.heading("scan_id", text="Номер скана")
    tree.heading("first_name", text="Имя")
    tree.heading("last_name", text="Фамилия")
    tree.heading("birth_date", text="Дата Рождения")
    tree.heading("more", text="Более")

    tree.column("scan_id", width=100, anchor='center')
    tree.column("first_name", width=150, anchor='center')
    tree.column("last_name", width=150, anchor='center')
    tree.column("birth_date", width=150, anchor='center')
    tree.column("more", width=100, anchor='center')

    scans = get_last_five_scans()
    for scan in scans:
        tree.insert("", "end",
                    values=(scan["scan_id"], scan["first_name"], scan["last_name"], scan["birth_date"], "Более"))

    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(history_window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_single_click(event):
        region = tree.identify("region", event.x, event.y)
        if region == "cell":
            column = tree.identify_column(event.x)
            if column == "#5":  # Пятый столбец "Более"
                row = tree.identify_row(event.y)
                if row:
                    scan_id = tree.item(row, "values")[0]
                    try:
                        scan_id = int(scan_id)
                    except ValueError:
                        messagebox.showerror("Ошибка", "Неверный ID скана.")
                        return
                    show_more_details(scan_id, history_window)

    tree.bind("<Button-1>", on_single_click)

    history_window.mainloop()

