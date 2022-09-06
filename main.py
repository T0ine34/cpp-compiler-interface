import tkinter as tk
from tkinter import ttk
import os
import sys

PATH = ''
print(PATH)

GCC_PATH = ''
CONFIG_PATH = 'config.conf'


def init():
    if not os.path.exists(GCC_PATH):
        GCC_PATH = ''




class input:
    class Text(tk.Toplevel):
        def __init__(self, master, text, var: tk.StringVar):
            self.var = var
            tk.Toplevel.__init__(self,master)

            self.frame = tk.Frame(self)
            self.label = tk.Label(self.frame, text=text)
            self.label.grid(column=0, row=0)
            self.input = tk.Entry(self.frame, textvariable=var)
            self.input.grid(column=1, row=0)
            self.frame.grid(column = 0,row = 0, columnspan = 2)

            self.ok_btn = tk.Button(self, text='Confirm', command=self.confirm, width = 10)
            self.quit_btn = tk.Button(self, text='Back', command=self.quit, width = 10)
            self.ok_btn.grid(row=1, column=0)
            self.quit_btn.grid(row=1, column=1)

            self.protocol('WM_DELETE_WINDOW', self.quit)

            self.bind('<Return>', self.confirm)
            self.bind('<Escape>', self.quit)
            
            master.wait_window(self)

        def quit(self, e=None):
            self.var.set('')
            self.destroy()

        def confirm(self, e=None):
            self.destroy()

    class Boolean(tk.Toplevel):
        def __init__(self, master, text, var:tk.BooleanVar):
            self.var = var
            tk.Toplevel.__init__(self, master)
            
            self.text = tk.Label(self, text = text)
            self.text.grid(row=0,column=0,columnspan=2)

            self.y_btn = tk.Button(self, text='Yes', command=self.yes, width = 10)
            self.n_btn = tk.Button(self, text = 'No', command=self.no, width = 10)
            self.y_btn.grid(row=1,column=0)
            self.n_btn.grid(row=1,column=1)
            
            master.wait_window(self)

        def yes(self,e=None):
            self.var.set(True)
            self.destroy()

        def no(self, e=None):
            self.var.set(False)
            self.destroy()

            

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        val = tk.StringVar()
        pr = tk.BooleanVar()
        input.Text(self, 'enter value :', val)
        input.Boolean(self, 'Print it ?', pr)
        if pr:
            print('-->',val.get())

main = Main()
main.mainloop()