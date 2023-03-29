
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
        funktion_menu.add_command(label='Trigonometrische',
                                  command=lambda: self.open_function_entry(fun.TermType.TRIGONOMETRISCH))
        menubar.add_cascade(
            label='neue Funktion',
            menu=funktion_menu
        )
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.grid(True, color='grey')
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.patch.set_edgecolor('grey')
        self.ax.patch.set_linewidth(1)
        self.ax.set_xlim(-1 * self.scale + self.offset_x, self.scale + self.offset_x)
        self.ax.set_ylim(-1 * self.scale + self.offset_y, self.scale + self.offset_y)
        self.ax.set_aspect('equal')
        yticklabels = self.ax.yaxis.get_major_ticks()
        yticklabels[round((len(yticklabels)-1) / 2)].label.set_visible(False)

        funcFrame = tk.Frame(self.root)
        funcFrame.pack(side="top", fill='both', expand=1)


        self.canvas = FigureCanvasTkAgg(self.fig, master=funcFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=1, side="right")

        self.frame_list_info = tk.Frame(funcFrame, width=50)
        self.frame_list_info.pack(side="left", fill='y')

        self.list_functions = tk.Listbox(self.frame_list_info, listvariable=self.funcListVar, width=50)
        self.list_functions.pack(side="top", fill="y")
        self.list_functions.bind('<<ListboxSelect>>', self.display_func_info)

        self.frame_info = tk.Frame(self.frame_list_info, width=50)
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



#   update
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
        self.ax.grid(True, color='grey')
        self.ax.spines['left'].set_position('center')
        self.ax.spines['bottom'].set_position('center')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.patch.set_edgecolor('grey')
        self.ax.patch.set_linewidth(1)
        self.ax.set_xlim(graphMinX, graphMaxX)
        self.ax.set_ylim(graphMinY, graphMaxY)
        yticklabels = self.ax.yaxis.get_major_ticks()
        yticklabels[round((len(yticklabels)-1) / 2)].label.set_visible(False)
        x_vals = np.linspace(graphMinX, graphMaxX, num=100)
        for function in self.functionList:
            y_vals = function.arr_calc(x_vals, fun.FunctionDerivative.ORIGINAL)
            self.ax.plot(x_vals, y_vals)
        self.canvas.draw()


    def update_window(self):
        self.update_list()
        self.update_canvas()
#   end

#   scaling
    def increment_scale(self):
        try:
            self.scale = float(self.scaleVar.get())
            self.scale += 10
            if self.scale <= 0:
                self.scale = 10
            self.update_window()
            self.scaleVar.set(str(self.scale))
        except Exception as e:
            print(e.args)

    def decrement_scale(self):
        try:
            self.scale = float(self.scaleVar.get())
            self.scale -= 10
            if self.scale <= 0:
                self.scale = 10
            self.update_window()
            self.scaleVar.set(str(self.scale))
        except Exception as e:
            print(e.args)

    def enter_scale(self, e):
        try:
            self.scale = float(self.scaleVar.get())
            if self.scale == 0:
                self.scale = 10
            self.update_window()
            self.scaleVar.set(str(self.scale))
        except Exception as e:
            print(e.args)
#   end

    def display_func_info(self, event):

        try:
            index = self.list_functions.curselection()[0]
        except IndexError:
            return

        func = self.functionList[index]
        list = self.frame_info.grid_slaves()
        for widget in list:
            widget.destroy()

        label = tk.Label(self.frame_info, text=f"{chr(ord('f') + index)}'(x)={func.deriv1_as_str()}")
        label.grid(row=0)

        label = tk.Label(self.frame_info, text=f"{chr(ord('f') + index)}''(x)={func.deriv2_as_str()}")
        label.grid(row=1)

        label = tk.Label(self.frame_info, text=f"{chr(ord('f') + index)}'''(x)={func.deriv3_as_str()}")
        label.grid(row=2)

        nullstellen_str = ""
        nullstellen_list = func.calc_nullstellen(fun.FunctionDerivative.ORIGINAL,
                                                 self.scale * -1, self.scale)
        null_list_len = len(nullstellen_list)
        print(null_list_len)
        for j in range(int(null_list_len / 10)):
            for i in range(10):
                nullstellen_str += f"N{fun.subscript_of(i + 1 + j *10)}({nullstellen_list[i]}|0) "
        label = tk.Label(self.frame_info, text=nullstellen_str)
        label.grid(row=3)





    def append_Function(self, fun, widget, event):
        if widget == event.widget:
            self.functionList.append(fun)
            self.update_window()

#   funktions eingabe
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
#   end

