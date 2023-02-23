import tkinter
import tkinter as tk
from logging import exception

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
        funktion_menu.add_command(label='lineare Funktion')
        funktion_menu.add_command(label='quadratische Funktion')
        funktion_menu.add_command(label='ganzrationale Funktion')
        menubar.add_cascade(
            label='Neue Funktion',
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
        frame_scale.pack(side="bottom", expand='x')

        ent_scale = tk.Entry(frame_scale, textvariable=self.scaleVar)
        ent_scale.bind("<Return>", func=self.enter_scale)
        ent_scale.pack(side="left")

        btn_increment_scale = tk.Button(frame_scale, text='+', command=self.increment_scale)
        btn_increment_scale.pack(side="left")

        btn_decrement_scale = tk.Button(frame_scale, text='-', command=self.decrement_scale)
        btn_decrement_scale.pack(side="left")

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


    def convert_factor_entry(self, factor: str) -> float:
        if factor[0] == '+':
            to_return = float(factor[1:])
            return to_return
        elif factor[0] == '-':
            to_return = -1 * float(factor[1:])
            return to_return
        else:
            raise ValueError("kein valides Vorzeichen")

    def linear_function(self):
        lin = tk.Tk()
        lin_factor = tk.StringVar()
        lin_const = tk.StringVar()

        entry_lin_factor = tk.Entry(lin, textvariable=lin_factor)
        entry_lin_factor.grid(column=0, row=1)

        label_lin_var = tk.Label(lin, text="x")
        label_lin_var.grid(column=1, row=1)

        entry_lin_const = tk.Entry(lin, textvariable=lin_const)
        entry_lin_const.grid(column=2, row=1)

        factor_0 = self.convert_factor_entry(entry_lin_const.get())
        factor_1 = self.convert_factor_entry()

        button_lin = tk.Button("eingabe", command= self.functionList.append(fun.Function()))
