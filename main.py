import tkinter as tk
from tkinter import ttk
import os
import sys
from pathlib import Path
from json import loads, dumps

import command as cmd

PATH = '\\'.join(str(Path(__file__).resolve()).split('\\')[:-1])
print(PATH)

CONFIG_PATH = 'config.conf'



class Parameters:
    def __init__(self):
        global CONFIG_PATH
        if not os.path.exists(PATH+'\\'+CONFIG_PATH):
            CONFIG_PATH = 'config.conf'
            f = open(PATH+'\\'+CONFIG_PATH, mode='w')
            f.write('{}')
            f.close()
        self.path = PATH+'\\'+CONFIG_PATH
        self.params = {}
        self.load()

    def load(self):
        with open(self.path, 'r') as file:
            self.params = loads(file.read())
    
    def save(self):
        with open(self.path, 'w') as file:
            file.write(dumps(self.params))

    def __getitem__(self,name):
        if name in self.params.keys():
            return str(self.params[name])
        else:
            self.params[name] = ''
            return str()

    def __getattibutes__(self, name):
        return self.params.__getattibutes__(name)


def init(master : tk.Tk) -> Parameters:
    param = Parameters()
    #TODO set here some work to do on startup
        
    return param

class Input:
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

class InputFn:
    def Text(master, text):
        var = tk.StringVar()
        Input.Text(master, text, var)
        return var.get()
    
    def Boolean(master, text):
        var = tk.BooleanVar()
        Input.Boolean(master, text, var)
        return var.get()
            

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.param = init(self)


        self.create_widgets()
        '''
        val = tk.StringVar()
        pr = tk.BooleanVar()
        Input.Text(self, 'enter value :', val)
        Input.Boolean(self, 'Print it ?', pr)
        if pr:
            print('-->',val.get())
        '''

    def create_widgets(self):
        pass

    def run(self):
        cmd.run(cmd.create_cmd())
        




main = Main()
main.mainloop()