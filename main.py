import json
import random
import string
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = 'password_history.json'

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.passwords = []

        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # Ползунок длины пароля
        ttk.Label(self.root, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(self.root, from_=4, to=32, orient='horizontal', variable=self.length_var, command=self.update_length_label)
        self.length_scale.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        self.length_label = ttk.Label(self.root, text="12")
        self.length_label.grid(row=0, column=2, padx=5, pady=5)

        # Чекбоксы для символов
        self.include_digits = tk.BooleanVar(value=True)
        self.include_letters = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=False)

        ttk.Checkbutton(self.root, text="Цифры (0-9)", variable=self.include_digits).grid(row=1, column=0, sticky='w', padx=5)
        ttk.Checkbutton(self.root, text="Буквы (A-Z, a-z)", variable=self.include_letters).grid(row=1, column=1, sticky='w', padx=5)
        ttk.Checkbutton(self.root, text="Спецсимволы", variable=self.include_special).grid(row=1, column=2, sticky='w', padx=5)

        # Генерация пароля
        generate_btn = ttk.Button(self.root, text="Генерировать пароль", command=self.generate_password)
        generate_btn.grid(row=2, column=0, columnspan=3, pady=10)

        # Поле для отображения сгенерированного пароля
        ttk.Label(self.root, text="Сгенерированный пароль:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.password_entry = ttk.Entry(self.root, width=50)
        self.password_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        # История
        ttk.Label(self.root, text="История паролей:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.tree = ttk.Treeview(self.root, columns=("Пароль", "Дата"), show='headings', height=10)
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        # Сохранить/Загрузить
        save_btn = ttk.Button(self.root, text="Сохранить историю", command=self.save_history)
        save_btn.grid(row=6, column=0, padx=5, pady=5)
        load_btn = ttk.Button(self.root, text="Загрузить историю", command=self.load_history)
        load_btn.grid(row=6, column=1, padx=5, pady=5)

    def update_length_label(self, event):
        self.length_label.config(text=str(int(self.length_var.get())))

    def generate_password(self):
        length = int(self.length_var.get())
        chars = ""

        if self.include_digits.get():
            chars += string.digits
        if self.include_letters.get():
            chars += string.ascii_letters
        if self.include_special.get():
            chars += string.punctuation

        if not chars:
            messagebox.showwarning("Внимание", "Выберите хотя бы один тип символов!")
            return

        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        # Добавляем в историю
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.passwords.append({"password": password, "date": now})
        self.refresh_history()

    def refresh_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for rec in self.passwords:
            self.tree.insert('', tk.END, values=(rec["password"], rec["date"]))

    def save_history(self):
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.passwords, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    def load_history(self):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.passwords = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.passwords = []
        self.refresh_history()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()