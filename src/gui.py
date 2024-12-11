import threading

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo, showwarning, showerror

from google_drive import gdrive


class Application(tk.Tk):
    choosen_dir: str = None

    def __init__(self):
        tk.Tk.__init__(self)
        self.set_ui()


    def set_ui(self):
        self.title("2GDArchiver")
        self.geometry("350x200")
        self.resizable(False, False)

        self.show_chooseh_dir()
        self.directory_button()
        self.upload_button()


    # Показ выбранной директории
    def show_chooseh_dir(self):
        text = self.choosen_dir

        if text is None: 
            text = "Директория не указана"

        self.path_label = ttk.Label(text=text)
        self.path_label.pack(pady=[40, 20])


    # Кнопка выбора директории
    def directory_button(self):
        self.dir_btn = ttk.Button(text="Выбрать директорию",
                                  command=self.get_dir)
        self.dir_btn.pack(fill="x", padx=50, pady=[0, 20])


    def get_dir(self):
        text = filedialog.askdirectory()
        
        if text != '':
            self.choosen_dir = text

        self.path_label.config(text=self.choosen_dir)


    # Отправка архива в GoogleDrive
    def upload_button(self):
        self.upload_btn = ttk.Button(text="Загрузить",
                                     command=lambda: threading.Thread(target=self.upload_dir).start())
        self.upload_btn.pack(fill="x", padx=50)


    def upload_dir(self):
        if self.choosen_dir is not None:
            self.upload_btn['state'] = 'disable'
            self.dir_btn['state'] = 'disable'

            result = gdrive.upload_file(self.choosen_dir)

            match result:
                case 0: showinfo(message="Отправка завершена успешно!")
                case -1: showerror(message="Некорректный файл для архивации!")
                case -2: showerror(message="Ошибка во время отправки")

            self.upload_btn['state'] = 'normal'
            self.dir_btn['state'] = 'normal'
            self.choosen_dir = None
            self.show_chooseh_dir()

        else:
            showwarning(title="Предупреждение",
                        message="Не выбрано хранилище!")
    

if __name__ == '__main__':
    root = Application()
    threading.Thread(target=root.mainloop())