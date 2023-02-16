import tkinter
import tkinter as tk

from matplotlib.backends.backend_tkagg import (
FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class GraphWindow:

    functionList: []
    scaleVar = tk.StringVar



    def __init__(self):


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

        self.fig, self.ax= plt.subplots(1,1)
        self.ax.grid(True)
        self.ax.set_xlim(-10,10)
        self.ax.set_ylim(-10,10)
        self.ax.set_aspect('equal')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=1)

        btn_increment_scale = tk.Button(text='+', command=self.increment_scale)
        btn_increment_scale.pack(side="bottom")

        btn_decrement_scale = tk.Button(text='-', command=self.decrement_scale)
        btn_decrement_scale.pack(side="bottom")

        ent_scale = tk.Entry(textvariable=self.scaleVar)
        ent_scale.bind("<Return>", func=self.enter_scale)
        ent_scale.pack(side="bottom")

        #listboxFunctions = tkinter.Listbox(root, listvariable=self.functionList, width=50)
        #listboxFunctions.pack(side="left", fill='y')

        root.mainloop()

    def increment_scale(self):
        print("increment")
        try:
            scale = float(self.scaleVar.get())
            scale += 10
            if scale == 0:
                scale = 10
            self.ax.set_xlim(-1 * scale, scale)
            self.ax.set_ylim(-1 * scale, scale)
            self.canvas.draw()
            self.scaleVar.set(str(scale))
        except:
            print("exception")


    def decrement_scale(self):
        print("decrement")
        try:
            scale = float(self.scaleVar.get())
            scale -= 10
            if scale==0:
                scale = -10
            self.ax.set_xlim(-1 * scale, scale)
            self.ax.set_ylim(-1 * scale, scale)
            self.canvas.draw()
            self.scaleVar.set(str(scale))
        except:
            print("exception")


    def enter_scale(self, e):
        try:
            scale = float(self.scaleVar.get())
            if scale == 0:
                scale = 10
            self.ax.set_xlim(-1 * scale, scale)
            self.ax.set_ylim(-1 * scale, scale)
            self.canvas.draw()
            self.scaleVar.set(str(scale))
        except:
            print("exception")
