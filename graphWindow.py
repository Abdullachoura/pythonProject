
import tkinter as tk

import matplotlib.axes

import Function as fun
import functionEntry as funent

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
        self.root = tk.Tk()
        self.scaleVar = tk.StringVar()
        self.scaleVar.set("10")
        self.funcListVar = tk.Variable(value=())

        self.root.title('Functional')

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        funktion_menu = tk.Menu(menubar)
        funktion_menu.add_command(label='selbst definierte Ganzrationale', command=lambda: self.rational_function())
        funktion_menu.add_command(label='Schnittpunktformel',
                                  command=lambda: self.open_function_entry(fun.TermType.SCHNITTPUNKT))
        funktion_menu.add_command(label='Trigonometrische')
        menubar.add_cascade(
            label='neue Funktion',
            menu=funktion_menu
        )
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.grid(True)
        self.ax.set_xlim(-1 * self.scale + self.offset_x, self.scale + self.offset_x)
        self.ax.set_ylim(-1 * self.scale + self.offset_y, self.scale + self.offset_y)
        self.ax.set_aspect('equal')

        funcFrame = tk.Frame(self.root)
        funcFrame.pack(side="top")


        self.canvas = FigureCanvasTkAgg(self.fig, master=funcFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=1, side="right")

        self.frame_list_info = tk.Frame(funcFrame)
        self.frame_list_info.pack(side="left", fill='y')

        self.list_functions = tk.Listbox(self.frame_list_info, listvariable=self.funcListVar)
        self.list_functions.pack(side="top", fill="y")

        self.frame_info = tk.Frame(self.frame_list_info)
        self.frame_info.pack(side='bottom')

        frame_scale = tk.Frame(master=self.root)
        frame_scale.pack(side="bottom", fill='x')

        ent_scale = tk.Entry(frame_scale, textvariable=self.scaleVar)
        ent_scale.bind("<Return>", func=self.enter_scale)
        ent_scale.pack(side="right")

        btn_increment_scale = tk.Button(frame_scale, text='+', command=self.increment_scale)
        btn_increment_scale.pack(side="right")

        btn_decrement_scale = tk.Button(frame_scale, text='-', command=self.decrement_scale)
        btn_decrement_scale.pack(side="right")
        self.root.mainloop()


    def update_list(self):
        list = ()
        funChar = ord('f')
        for fun in self.functionList:
            list = list + (f"{chr(funChar)}(x)=" + str(fun),)
            funChar += 1
        self.funcListVar.set(list)

    def update_canvas(self):
        graphMinX = -1 * self.scale + self.offset_x
        graphMaxX = self.scale + self.offset_x
        graphMinY = -1 * self.scale + self.offset_y
        graphMaxY = self.scale + self.offset_y
        self.ax.clear()
        self.ax.grid(True)
        self.ax.set_xlim(graphMinX, graphMaxX)
        self.ax.set_ylim(graphMinY, graphMaxY)
        x_vals = np.linspace(graphMinX, graphMaxX)
        for function in self.functionList:
            y_vals = function.arr_calc(x_vals, fun.FunctionDerivative.ORIGINAL)
            self.ax.plot(x_vals, y_vals)
        self.canvas.draw()


    def update_window(self):
        self.update_list()
        self.update_canvas()


    def increment_scale(self):
        try:
            self.scale = float(self.scaleVar.get())
            self.scale += 10
            if self.scale <= 0:
                self.scale = 10
            self.update_window()
            self.scaleVar.set(str(self.scale))
        except:
            print("exception")

    def decrement_scale(self):
        try:
            self.scale = float(self.scaleVar.get())
            self.scale -= 10
            if self.scale <= 0:
                self.scale = 10
            self.update_window()
            self.scaleVar.set(str(self.scale))
        except:
            print("exception")

    def enter_scale(self, e):
        try:
            self.scale = float(self.scaleVar.get())
            if self.scale == 0:
                self.scale = 10
            self.update_window()
            self.scaleVar.set(str(self.scale))
        except:
            print("exception")


    def append_Function(self, fun, widget, event):
        if widget == event.widget:
            self.functionList.append(fun)
            self.update_window()

    def open_function_entry(self, term_type: fun.TermType, *args):
        fun_entry_win = funent.FunctionEntry(term_type, *args)
        fun_entry_win.root.bind("<Destroy>", lambda x: self.append_Function(fun_entry_win.func, fun_entry_win.root, x))
        fun_entry_win.root.mainloop()
        self.functionList.append(fun_entry_win.func)

    def rational_function_button_event(self, root:tk.Tk,  termType:fun.TermType, *args):
        root.destroy()
        self.open_function_entry(termType, *args)

    def rational_function(self):
        root = tk.Tk()
        root.title('Funktionsgrad angabe')
        text_var = tk.StringVar()
        label = tk.Label(root, text='gewünschter Funktionsgrad:')
        label.pack(side='left')
        entry = tk.Entry(root, textvariable=text_var)
        entry.pack(side='left')
        button = tk.Button(root, text='Eingeben',
                           command=lambda: self.rational_function_button_event(root,
                                                                               fun.TermType.GANZ_RATIONAL,
                                                                               int(entry.get())))
        button.pack(side='left')
        root.mainloop()


