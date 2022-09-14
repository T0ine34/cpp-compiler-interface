
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import sys
from pathlib import Path
from json import loads, dumps

import command as cmd

PATH = '\\'.join(str(Path(__file__).resolve()).split('\\')[:-1])


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
            print('"'+name+'" do not exist in '+CONFIG_PATH+' : creating it and set it to ""')
            self.params[name] = ''
            self.save()
            return str()

    def __getattibutes__(self, name):
        return self.params.__getattibutes__(name)

    def get(self, name):
        return self.__getitem__(name)


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
        self.input_frame = Widgets.InputFrame(self)
        self.output_frame = Widgets.OutputFrame(self)
        self.type_output = Widgets.Output_Type(self, self.output_frame.set_extension)
        self.show_err = Widgets.Show_err(self)
        self.button = Widgets.Compile_Button(self)

        self.type_output.grid(row=0, column = 0)
        self.show_err.grid(row = 0, column = 1)
        self.input_frame.grid(row = 1, column = 0, columnspan=2)
        self.output_frame.grid(row = 2, column = 0, columnspan=2)
        self.button.grid(row = 3, column = 0, columnspan=2)

    def run(self):
        input = self.input_frame.get()
        output = self.output_frame.get()
        operation = self.type_output.get()
        show_err = self.show_err.get()

        temp_path = self.param.get('temp_path')

        cmd.compile(input, output, operation, show_err, temp_path)
        

class Widgets:
    class InputFrame(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self,master)
            self.value = tk.StringVar()
            self.paths = []
            self.label = tk.Label(self, textvariable=self.value, width= 50)
            self.label.grid(row = 0, column = 0)

            self.button = tk.Button(self, text = 'Choose files to compile', command=self.open_window, width= 25)
            self.button.grid(row = 0, column = 1)

        def open_window(self, c=None):
            value = filedialog.askopenfilename(title='Choose files to compile', multiple=True, filetypes= (('C++', '*.cpp'),('O', '*.o')), initialdir=self.master.param.get('default_input'))
            if value is not None:
                self.paths = value
                self.value.set(value)
        
        def get(self) -> list:
            return self.paths

    class OutputFrame(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self,master)

            self.ftypes = [("All Files", "*.*")]

            self.value = tk.StringVar()
            self.label = tk.Label(self, textvariable=self.value, width= 50)
            self.label.grid(row = 0, column = 0)

            self.button = tk.Button(self, text = 'Choose location of compiled file', command=self.open_window, width= 25)
            self.button.grid(row = 0, column = 1)

        def open_window(self, c=None):
            value = filedialog.asksaveasfilename(title='Choose location of compiled file', filetypes= self.ftypes, initialdir=self.master.param.get('default_output'))
            if value is not None:
                self.value.set(value)

        def get(self):
            return self.value.get()

        def set_extension(self, extension):
            if extension == 'Executable (.exe)':
                self.ftypes = [('Executable','*.exe'),("All Files", "*.*")] 
            elif extension == 'Assembly (.s)':
                self.ftypes = [('Assembly', '*.s'),("All Files", "*.*")] 
            elif extension == 'Compiled file (.o)':
                self.ftypes = [('Compiled File','*.o'),("All Files", "*.*")] 
            elif extension == 'Shared library (.so)':
                self.ftypes = [('Shared library','*.so'),("All Files", "*.*")] 
            

    class Output_Type(tk.Frame):
        def __init__(self, master, cmd):
            self.cmd = cmd
            tk.Frame.__init__(self,master)
            self.box = ttk.Combobox(self, state='readonly', values=('Executable (.exe)', 'Assembly (.s)', 'Compiled file (.o)', 'Shared library (.so)'))
            self.box.current(0)
            self.command()
            self.box.bind('<<ComboboxSelected>>', self.command)
            self.box.pack()

        def get(self):
            return self.box.get()

        def command(self, c = None):
            #execute the function passed as cmd parameter, with the value of the combobox
            self.cmd(self.get())
            
    class Show_err(tk.Frame):
        def __init__(self, master):
            self.value = tk.BooleanVar()
            tk.Frame.__init__(self,master)
            self.label = tk.Label(self, text = 'Show errors ?')
            self.box = ttk.Checkbutton(self, variable=self.value, onvalue=True, offvalue=False)
            
            self.label.grid(row = 0, column = 0)
            self.box.grid(row = 0, column = 1)

        def get(self):
            return self.value.get()

    class Compile_Button(tk.Button):
        def __init__(self, master):
            tk.Button.__init__(self,master, text='Compile', command=self.cmd)

        def cmd(self):
            self.master.run()

main = Main()
main.mainloop()