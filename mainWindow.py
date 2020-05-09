import tkinter as tk
from tkinter import ttk
import sqlite3

background = '#d7d8e0'


def open_dialog():
    Child()


class Main(tk.Frame):
    def __init__(self, myRoot):
        super().__init__(myRoot)
        self.tree = ttk.Treeview(self, columns=('ID', 'desc', 'cost', 'total'), height=16, show='headings')
        self.add_img = tk.PhotoImage(file='check.gif')
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg=background, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Добавить', command=open_dialog,
                                    bg=background, bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('desc', width=365, anchor=tk.CENTER)
        self.tree.column('cost', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('desc', text='Наименование')
        self.tree.heading('cost', text='Доход/расход')
        self.tree.heading('total', text='Сумма')

        self.tree.pack()

    def records(self, desc, cost, total):
        self.db.insert_data(desc, cost, total)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM finance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'])
        self.entry_money = ttk.Entry(self)
        self.entry_desc = ttk.Entry(self)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Дочернее окно')
        self.geometry('400x220+400+200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_desc = tk.Label(self, text='Наименование')
        label_money = tk.Label(self, text='Доход/расход')
        label_combobox = tk.Label(self, text='Сумма:')

        label_desc.place(x=50, y=50)
        label_money.place(x=50, y=110)
        label_combobox.place(x=50, y=80)
        self.entry_desc.place(x=200, y=50)
        self.entry_money.place(x=200, y=110)
        self.combobox.place(x=200, y=80)

        self.combobox.current(0)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_ok = tk.Button(self, text='Добавить')

        btn_cancel.place(x=300, y=170)
        btn_ok.place(x=220, y=170)

        btn_ok.bind('<Button-1>', lambda event: self.view.records(
            self.entry_desc.get(), self.entry_money.get(), self.combobox.get()
        ))


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS finance (
            id integer primary key,
            desc text,
            cost text,
            total real)'''
        )
        self.conn.commit()

    def insert_data(self, desc, cost, total):
        self.c.execute(
            '''INSERT INTO finance(desc, cost, total)
            VALUES (?, ?, ?)''', (desc, cost, total))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Главное окно")
    root.geometry('640x480+300+100')
    root.resizable(False, False)
    root.mainloop()
