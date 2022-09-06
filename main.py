import tkinter as tk
from tkinter import ttk
import os
import sys

class input(tk.Toplevel):
    def __init__(self, master, text, var: tk.StringVar):
        tk.Toplevel.__init__(self,master)

        self.label = tk.Label(self, text=text)
        self.label.grid()
        self.input = tk.Entry(self, )


class main(tk.Tk):
    def __init__(self):
        pass