import tkinter as tk
from tkinter import ttk
import sqlite3

background = '#d7d8e0'


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg=background, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='check.gif')
        btn_open_dialog = tk.Button(toolbar, text='Добавить', command=self.open_dialog,
                                    bg=background, bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'desc', 'cost', 'total'), height=16, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('desc', width=365, anchor=tk.CENTER)
        self.tree.column('cost', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('desc', text='Наименование')
        self.tree.heading('cost', text='Доход/расход')
        self.tree.heading('total', text='Сумма')

        self.tree.pack()

    def open_dialog(self):
        Child()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()

    def init_child(self):
        self.title('Дочернее окно')
        self.geometry('400x220+400+200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_desc = tk.Label(self, text='Наименование')
        label_desc.place(x=50, y=50)
        label_money = tk.Label(self, text='Доход/расход')
        label_money.place(x=50, y=110)
        label_combobox = tk.Label(self, text='Сумма:')
        label_combobox.place(x=50, y=80)

        self.entry_desc = ttk.Entry(self)
        self.entry_desc.place(x=200, y=50)

        self.entry_money = ttk.Entry(self)
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = tk.Button(self, text='Добавить')
        btn_ok.place(x=220, y=170)
        btn_ok.bind('<Button-1>')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute(
            ''''CREATE TABLE IF NOT EXISTS finance (
            id integer primary key,
            desc text,
            cost text,
            total real)'''
        )
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Главное окно")
    root.geometry('640x480+300+100')
    root.resizable(False, False)
    root.mainloop()
