import tkinter
import tkinter as tk
import tkinter.menu
import function as fun

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class GraphWindow:
    functionList: []
    scaleVar = tk.StringVar
    scale: float
    offset_x: float
    offset_y: float

    def __init__(self):
        self.scale = 10
        self.offset_x = 0
        self.offset_y = 0
        self.functionList = []
        root = tk.Tk()
        self.scaleVar = tk.StringVar()
        self.scaleVar.set("10")

        root.title('Functional')

        menubar = tk.Menu(root)
        root.config(menu=menubar)
        funktion_menu = tk.Menu(menubar)
        funktion_menu.add_command(label='1', command=self.rational_function(1))
        funktion_menu.add_command(label='2', command=self.rational_function(2))
        funktion_menu.add_command(label='3', command=self.rational_function(3))
        funktion_menu.add_command(label='4', command=self.rational_function(4))
        funktion_menu.add_command(label='selbst definiert', command=self.rational_function(-1))
        funktion_menu.add(itemType=tkinter.Menu)
        menubar.add_cascade(
            label='ganzrationale Funktion',
            menu=funktion_menu
        )

        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.grid(True)
        self.ax.set_xlim(-1 * self.scale + self.offset_x, self.scale + self.offset_x)
        self.ax.set_ylim(-1 * self.scale + self.offset_y, self.scale + self.offset_y)
        self.ax.set_aspect('equal')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=1)

        frame_scale = tk.Frame(master=root)
        frame_scale.pack(side="bottom", fill='x')

        ent_scale = tk.Entry(frame_scale, textvariable=self.scaleVar)
        ent_scale.bind("<Return>", func=self.enter_scale)
        ent_scale.pack(side="right")

        btn_increment_scale = tk.Button(frame_scale, text='+', command=self.increment_scale)
        btn_increment_scale.pack(side="right")

        btn_decrement_scale = tk.Button(frame_scale, text='-', command=self.decrement_scale)
        btn_decrement_scale.pack(side="right")

        # listboxFunctions = tkinter.Listbox(root, listvariable=self.functionList, width=50)
        # listboxFunctions.pack(side="left", fill='y')

        root.mainloop()

    def draw(self):
        self.ax.set_xlim(-1 * self.scale + self.offset_x, self.scale + self.offset_x)
        self.ax.set_ylim(-1 * self.scale + self.offset_y, self.scale + self.offset_y)
        self.canvas.draw()

    def increment_scale(self):
        try:
            self.scale = float(self.scaleVar.get())
            self.scale += 10
            if self.scale <= 0:
                self.scale = 10
            self.draw()
            self.scaleVar.set(str(self.scale))
        except:
            print("exception")

    def decrement_scale(self):
        try:
            self.scale = float(self.scaleVar.get())
            self.scale -= 10
            if self.scale <= 0:
                self.scale = 10
            self.draw()
            self.scaleVar.set(str(self.scale))
        except:
            print("exception")

    def enter_scale(self, e):
        try:
            self.scale = float(self.scaleVar.get())
            if self.scale == 0:
                self.scale = 10
            self.draw()
            self.scaleVar.set(str(self.scale))
        except:
            print("exception")

    def rational_function(self, n):
        if n==-1:
            root = tk.Tk()
            root.title('Funktionsgrad angabe')

            text_var = tk.StringVar()

            label= tk.Label(root, text='gewünschter Funktionsgrad:')
            label.pack(side='left')

            entry = tk.Entry(root, textvariable=text_var)
            entry.pack(side='left')

            button = tk.Button(root, text='Eingeben', command=)
            button.pack(side='left')

            root.mainloop()




