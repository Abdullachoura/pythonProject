import sys
import tkinter.messagebox as msgbox
import tkinter as tk
import types

import function as fun
import functionEntry as funent
import scalebarFunktionChange as sfc

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class GraphWindow:
    functionList: []
    scaleVar = tk.StringVar
    scale: float
    offset_x: float
    offset_y: float

    def __init__(self):
        self.scale = 20
        self.offset_x = 0
        self.offset_y = 0
        self.functionList = [fun.Function(fun.TermType.GANZ_RATIONAL, 2, -2),
                             fun.Function(fun.TermType.SCHNITTPUNKT, 1, -1, -5),
                             fun.Function(fun.TermType.TRIGONOMETRISCH, fun.TrigonometrischerOperator.SIN, 5, 0, 10),
                             fun.Function(fun.TermType.EXPONENTIEL, 2)]
        self.nullstellen_list = []
        self.extremstellen_list = []
        self.wendestellen_list = []
        self.selected_function = None
        self.selected_index = None
        self.root = tk.Tk()
        self.scaleVar = tk.StringVar()
        self.scaleVar.set("20")
        self.offset_y_Var = tk.StringVar()
        self.offset_y_Var.set("0")
        self.offset_x_Var = tk.StringVar()
        self.offset_x_Var.set("0")
        self.funcListVar = tk.Variable(value=())
        self.nullstellenListVar = tk.Variable(value=())
        self.extrempunkteListVar = tk.Variable(value=())
        self.wendepunkteListVar = tk.Variable(value=())

        self.root.title('Functional')
        self.root.bind('<Destroy>', self.on_close)
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        funktion_menu = tk.Menu(menubar)
        funktion_menu.add_command(label='selbst definierte Ganzrationale', command=lambda: self.rational_function())
        funktion_menu.add_command(label='Schnittpunktformel',
                                  command=lambda: self.open_function_entry(fun.TermType.SCHNITTPUNKT))
        funktion_menu.add_command(label='Trigonometrische',
                                  command=lambda: self.open_function_entry(fun.TermType.TRIGONOMETRISCH))
        funktion_menu.add_command(label="Exponentiele Funktion",
                                  command=lambda: self.open_function_entry(fun.TermType.EXPONENTIEL))
        menubar.add_cascade(
            label='neue Funktion',
            menu=funktion_menu
        )
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.grid(True, color='grey')
        self.ax.spines['left'].set_position(('data', 0))
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.patch.set_edgecolor('grey')
        self.ax.patch.set_linewidth(1)
        self.ax.set_xlim(-1 * self.scale / 2 + self.offset_x, self.scale / 2 + self.offset_x)
        self.ax.set_ylim(-1 * self.scale / 2 + self.offset_y, self.scale / 2 + self.offset_y)
        self.ax.set_aspect('equal')
        yticklabels = self.ax.yaxis.get_major_ticks()
        yticklabels[round((len(yticklabels)-1) / 2)].label.set_visible(False)

        func_info_Frame = tk.Frame(self.root)
        func_info_Frame.pack(side='top', fill='both', expand=1)

        funcFrame = tk.Frame(func_info_Frame)
        funcFrame.pack(side="right", fill='both', expand=True)

        button = tk.Button(funcFrame, text=chr(0x21E7), command=lambda: self.increment_yoffset(1))
        button.pack(side='top', fill='x')

        button = tk.Button(funcFrame, text=chr(0x21E9), command=lambda: self.decrement_yoffset(1))
        button.pack(side='bottom', fill='x')

        button = tk.Button(funcFrame, text=chr(0x21E6), command=lambda: self.decrement_xoffset(1))
        button.pack(side='left', fill='y')

        self.canvas = FigureCanvasTkAgg(self.fig, master=funcFrame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=1, side="left")

        button = tk.Button(funcFrame, text=chr(0x21E8), command=lambda: self.increment_xoffset(1))
        button.pack(side='right', fill='y')

        self.frame_list_info = tk.Frame(func_info_Frame, width=50)
        self.frame_list_info.pack(side="left", fill='y')

        frame_list = tk.Frame(self.frame_list_info)
        frame_list.pack(side='top', fill='both', expand=True)

        self.listbox_function_contextmenu = tk.Menu(self.root, tearoff=0)
        self.change_function_param_menu = tk.Menu(self.listbox_function_contextmenu)
        self.change_function_param_menu.add_command(label="Funktions eingabefenster",
                                                    command=self.change_function_parameters_ent)
        self.change_function_param_menu.add_command(label="SKalliertbalken", command=self.change_function_scalebar)
        self.listbox_function_contextmenu.add_command(label="Entfehrnen", command=self.remove_function)
        self.listbox_function_contextmenu.add_cascade(label="Bearbeiten", menu=self.change_function_param_menu)
        self.listbox_function_contextmenu.add_command(label="Integral berechen", command=self.open_integral_calc)

        label = tk.Label(frame_list, text='Funktionen')
        label.pack(side='top')
        self.listbox_functions = tk.Listbox(frame_list, listvariable=self.funcListVar, width=50)
        self.listbox_functions.pack(side="left", fill="both", expand=True)
        self.listbox_functions.bind('<<ListboxSelect>>', self.functionlist_item_selected, add='+')
        self.listbox_functions.bind('<Button-3>', self.popup, add='+')

        scrollbar = tk.Scrollbar(frame_list, orient='vertical')
        scrollbar.config(command=self.listbox_functions.yview)
        scrollbar.pack(side='right', fill='both')
        self.listbox_functions.config(yscrollcommand=scrollbar.set, width=50)

        label = tk.Label(self.frame_list_info, text="ableitungen")
        label.pack(side='top')
        self.frame_ableitungen = tk.Frame(self.frame_list_info, width=50)
        self.frame_ableitungen.pack(side='top')

        frame_stellen = tk.Frame(self.frame_list_info)
        frame_stellen.pack(side='bottom')

        frame_nullstellen_list = tk.Frame(frame_stellen)
        frame_nullstellen_list.pack(side='left')
        label = tk.Label(frame_nullstellen_list, text='Nullstellen')
        label.pack(side='top')
        self.nullstellen_label = tk.Label(frame_nullstellen_list, text='', borderwidth=1)
        self.nullstellen_label.pack(side='bottom')
        self.list_nullstellen = tk.Listbox(frame_nullstellen_list, listvariable=self.nullstellenListVar)
        self.list_nullstellen.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(frame_nullstellen_list, orient='vertical')
        scrollbar.config(command=self.list_nullstellen.yview)
        scrollbar.pack(side='right', fill='both')
        self.list_nullstellen.config(yscrollcommand=scrollbar.set)

        frame_extremstellen_list = tk.Frame(frame_stellen)
        frame_extremstellen_list.pack(side='left')
        label = tk.Label(frame_extremstellen_list, text='Extremstellen')
        label.pack(side='top')
        self.extremstellen_label = tk.Label(frame_extremstellen_list, text='', borderwidth=1)
        self.extremstellen_label.pack(side='bottom')
        list_extremstellen = tk.Listbox(frame_extremstellen_list, listvariable=self.extrempunkteListVar)
        list_extremstellen.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(frame_extremstellen_list, orient='vertical')
        scrollbar.config(command=list_extremstellen.yview)
        scrollbar.pack(side='right', fill='both')
        list_extremstellen.config(yscrollcommand=scrollbar.set)

        frame_wendestellen_list = tk.Frame(frame_stellen)
        frame_wendestellen_list.pack(side='left')
        label = tk.Label(frame_wendestellen_list, text='Wendestellen')
        label.pack(side='top')
        self.wendestellen_label = tk.Label(frame_wendestellen_list, text='', borderwidth=1)
        self.wendestellen_label.pack(side='bottom')
        list_wendestellen = tk.Listbox(frame_wendestellen_list, listvariable=self.wendepunkteListVar)
        list_wendestellen.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(frame_wendestellen_list, orient='vertical')
        scrollbar.config(command=list_wendestellen.yview)
        scrollbar.pack(side='right', fill='both')
        list_wendestellen.config(yscrollcommand=scrollbar.set)

        frame_scale = tk.Frame(master=self.root)
        frame_scale.pack(side="bottom", fill='x')

        btn_decrement_scale = tk.Button(frame_scale, text='-', command=self.decrement_scale)
        btn_decrement_scale.pack(side="right")

        btn_increment_scale = tk.Button(frame_scale, text='+', command=self.increment_scale)
        btn_increment_scale.pack(side="right")

        ent_scale = tk.Entry(frame_scale, textvariable=self.scaleVar)
        ent_scale.bind("<Return>", func=self.enter_scale)
        ent_scale.pack(side="right")

        label = tk.Label(frame_scale, text='Skallierung:')
        label.pack(side='right')

        label = tk.Label(frame_scale, text='x Verschiebung:')
        label.pack(side='left')

        ent_xoffset = tk.Entry(frame_scale, textvariable=self.offset_x_Var)
        ent_xoffset.pack(side="left")
        ent_xoffset.bind("<<Return>>", self.enter_xoffset)

        btn_increment_xoffset = tk.Button(frame_scale, text='+', command=lambda: self.increment_xoffset(10))
        btn_increment_xoffset.pack(side='left')

        btn_decrement_xoffset = tk.Button(frame_scale, text='-', command=lambda: self.decrement_xoffset(10))
        btn_decrement_xoffset.pack(side='left')

        label = tk.Label(frame_scale)
        label.pack(side='left', padx=10)

        label = tk.Label(frame_scale, text='y-Verschiebung:')
        label.pack(side='left')

        ent_yoffset = tk.Entry(frame_scale, textvariable=self.offset_y_Var)
        ent_yoffset.pack(side='left')
        ent_yoffset.bind("<<Return>>", self.enter_yoffset)

        btn_increment_yoffset = tk.Button(frame_scale, text='+', command=lambda: self.increment_yoffset(10))
        btn_increment_yoffset.pack(side='left')

        btn_decrement_yoffset = tk.Button(frame_scale, text='-', command=lambda: self.decrement_yoffset(10))
        btn_decrement_yoffset.pack(side='left')

        self.update_window()
        self.root.mainloop()

    def on_close(self, event):
        if event.widget == self.root:
            sys.exit()

#   update
    def update_list(self):
        list = ()
        funChar = ord('f')
        for fun in self.functionList:
            list = list + (f"{chr(funChar)}(x)=" + str(fun),)
            funChar += 1
        self.funcListVar.set(list)

    def update_canvas(self):
        graphMinX = -1 * self.scale / 2 + self.offset_x
        graphMaxX = self.scale / 2 + self.offset_x
        graphMinY = -1 * self.scale / 2 + self.offset_y
        graphMaxY = self.scale / 2 + self.offset_y
        self.ax.clear()
        self.ax.grid(True, color='grey')
        self.ax.spines['left'].set_position(('data', 0))
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.patch.set_edgecolor('grey')
        self.ax.patch.set_linewidth(1)
        self.ax.set_xlim(graphMinX, graphMaxX)
        self.ax.set_ylim(graphMinY, graphMaxY)

        x_vals = np.linspace(graphMinX, graphMaxX, num=100)
        for i in range(len(self.functionList)):
            y_vals = self.functionList[i].arr_calc(x_vals, fun.FunctionDerivative.ORIGINAL)
            self.ax.plot(x_vals, y_vals, label=f'{chr(ord("f") + i)}')

        if isinstance(self.selected_function, fun.Function):
            for i in range(len(self.nullstellen_list)):
                self.ax.plot(self.nullstellen_list[i][0], 0, 'bo')
                self.ax.text(self.nullstellen_list[i][0] + 0.02, self.nullstellen_list[i][1] + 0.02,
                             f'N{fun.subscript_of(i + 1)}')

            tp_i = 1
            hp_i = 1
            for i in range(len(self.extremstellen_list)):
                if self.extremstellen_list[i][0] > 0:
                    self.ax.plot(self.extremstellen_list[i][1][0], self.extremstellen_list[i][1][1], 'bo')
                    self.ax.text(self.extremstellen_list[i][1][0] + 0.02, self.extremstellen_list[i][1][1] + 0.02,
                                 f'TP{fun.subscript_of(tp_i)}')
                    tp_i += 1
                elif self.extremstellen_list[i][0] < 0:
                    self.ax.plot(self.extremstellen_list[i][1][0], self.extremstellen_list[i][1][1], 'bo')
                    self.ax.text(self.extremstellen_list[i][1][0] + 0.02, self.extremstellen_list[i][1][1] + 0.02,
                                 f'HP{fun.subscript_of(hp_i)}')
                    hp_i += 1
            if not isinstance(self.selected_function.term, fun.TrigonomischerTerm):
                for i in range(len(self.wendestellen_list)):
                    self.ax.plot(self.wendestellen_list[i][0], self.wendestellen_list[i][1], 'bo')
                    self.ax.text(self.wendestellen_list[i][0] + 0.02, self.wendestellen_list[i][1] + 0.02,
                                 f'WP{fun.subscript_of(i + 1)}')
        self.ax.legend()
        self.canvas.draw()


    def update_window(self):
        self.update_list()
        self.update_func_info_frames(self.selected_function, self.selected_index)
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

    def increment_yoffset(self, amount):
        self.offset_y += amount
        self.offset_y_Var.set(str(self.offset_y))
        self.update_canvas()

    def decrement_yoffset(self, amount):
        self.offset_y -= amount
        self.offset_y_Var.set(str(self.offset_y))
        self.update_canvas()

    def enter_yoffset(self):
        offset_y_str = self.offset_y_Var.get()
        self.offset_y = float(offset_y_str)

    def increment_xoffset(self, amount):
        self.offset_x += amount
        self.offset_x_Var.set(str(self.offset_x))
        self.update_canvas()

    def decrement_xoffset(self, amount):
        self.offset_x -= amount
        self.offset_x_Var.set(str(self.offset_x))
        self.update_canvas()

    def enter_xoffset(self):
        offset_x_str = self.offset_x_Var.get()
        self.offset_x = float(offset_x_str)
#   end

    def update_func_info_frames(self, func, index):

        self.nullstellen_label.config(text='')
        self.extremstellen_label.config(text='')
        self.wendestellen_label.config(text='')
        list = self.frame_ableitungen.grid_slaves()
        for widget in list:
            widget.destroy()

        if isinstance(func, types.NoneType) or isinstance(index, types.NoneType):
            self.nullstellenListVar.set(())
            self.extrempunkteListVar.set(())
            self.wendepunkteListVar.set(())
            return

        label = tk.Label(self.frame_ableitungen, text=f"{chr(ord('f') + index)}'(x)={func.deriv1_as_str()}")
        label.grid(row=0)

        label = tk.Label(self.frame_ableitungen, text=f"{chr(ord('f') + index)}''(x)={func.deriv2_as_str()}")
        label.grid(row=1)

        label = tk.Label(self.frame_ableitungen, text=f"{chr(ord('f') + index)}'''(x)={func.deriv3_as_str()}")
        label.grid(row=2)

        try:
            nullstellen_list = func.calc_nullstellen(fun.FunctionDerivative.ORIGINAL,
                                                     self.scale / 2 * -1 + self.offset_x, self.scale / 2 + self.offset_x)
            if isinstance(nullstellen_list, types.NoneType):
                self.nullstellen_list.clear()
                self.nullstellenListVar.set(())
                self.nullstellen_label.config(text="|keine Nullstellen")
            else:
                nullstellen = []
                for i in range(len(nullstellen_list)):
                    nullstellen.append(f"N{fun.subscript_of(i + 1)}{nullstellen_list[i]}")
                self.nullstellenListVar.set(nullstellen)
                self.nullstellen_list = nullstellen_list
        except ValueError as ve:
            self.nullstellen_list.clear()
            self.nullstellenListVar.set(())
            self.nullstellen_label.config(text=f"|{ve.args[0]}")
        try:
            extrempunkte_list = func.calc_extrempunkte(self.scale / 2 * -1 + self.offset_x, self.scale / 2 + self.offset_x)
            if isinstance(extrempunkte_list, types.NoneType):
                self.extremstellen_list.clear()
                self.extrempunkteListVar.set(())
                self.extremstellen_label.config(text="keine extrempunkte")
            else:
                deriv2_extrempunkte_y= []
                for i in range(len(extrempunkte_list)):
                    deriv2_extrempunkte_y.append(func.calc_deriv2(extrempunkte_list[i][0]))
                print("deriv3_für_extrempunkte", deriv2_extrempunkte_y)
                extrempunkte = []
                tp_i = 1
                hp_i = 1
                for i in range(len(extrempunkte_list)):
                    if deriv2_extrempunkte_y[i] > 0:
                        extrempunkte.append(f"TP{fun.subscript_of(tp_i)}{extrempunkte_list[i]}")
                        tp_i += 1
                    elif deriv2_extrempunkte_y[i] < 0:
                        extrempunkte.append(f"HP{fun.subscript_of(hp_i)}{extrempunkte_list[i]}")
                        hp_i += 1
                self.extrempunkteListVar.set(extrempunkte)
                self.extremstellen_list = [(np.sign(func.calc_deriv2(extrempunkte_list[i][0])),
                                            extrempunkte_list[i]) for i in range(len(extrempunkte_list))]
                '''
                for i in range(len(extrempunkte_list)):
                    if deriv3_für_extrempunkte[i] > 0:
                        self.ax.plot(extrempunkte_list[i][0], extrempunkte_list[i][1], 'bo')
                        self.ax.text(extrempunkte_list[i][0] + 0.02, extrempunkte_list[i][1] + 0.02,
                                     f'TP{fun.subscript_of(tp_i)}')
                        tp_i += 1
                    elif deriv3_für_extrempunkte[i] < 0:
                        self.ax.plot(extrempunkte_list[i][0], extrempunkte_list[i][1], 'bo')
                        self.ax.text(extrempunkte_list[i][0] + 0.02, extrempunkte_list[i][1] + 0.02,
                                     f'HP{fun.subscript_of(hp_i)}')
                        hp_i += 1
                '''
        except ValueError as ve:
            self.extremstellen_list.clear()
            self.extrempunkteListVar.set(())
            self.extremstellen_label.config(text=f"|{ve.args[0]}")
        try:
            wendepunkte_list = func.calc_wendepunkte(self.scale / 2 * -1 + self.offset_x,
                                                     self.scale / 2 + self.offset_x)
            if isinstance(wendepunkte_list, types.NoneType):
                self.wendestellen_list.clear()
                self.wendepunkteListVar.set(())
                self.wendestellen_label.config(text="|keine wendepunkte im Koordinatensystem")
            else:
                wendepunkte = []
                for i in range(len(wendepunkte_list)):
                    wendepunkte.append(f"WP{fun.subscript_of(i + 1)}{wendepunkte_list[i]}")
                self.wendepunkteListVar.set(wendepunkte)
                self.wendestellen_list = wendepunkte_list
                '''
                for i in range(len(wendepunkte_list)):
                    self.ax.plot(wendepunkte_list[i][0], wendepunkte_list[i][1], 'bo')
                    self.ax.text(wendepunkte_list[i][0] + 0.02, wendepunkte_list[i][1] + 0.02,
                                 f'WP{fun.subscript_of(i)}')
                '''
        except ValueError as ve:
            self.wendestellen_list.clear()
            self.wendepunkteListVar.set(())
            self.wendestellen_label.config(text=f"|{ve.args[0]}")

    def functionlist_item_selected(self, event):
        self.listbox_function_contextmenu.unpost()
        self.selected_index = self.listbox_functions.curselection()[0]
        self.selected_function = self.functionList[self.selected_index]
        self.update_window()


    def popup(self, event):
        self.listbox_functions.selection_clear(0, tk.END)
        self.listbox_functions.selection_set(self.listbox_functions.nearest(event.y))
        self.listbox_functions.activate(self.listbox_functions.nearest(event.y))
        self.selected_index = self.listbox_functions.curselection()[0]
        self.selected_function = self.functionList[self.selected_index]
        self.listbox_function_contextmenu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
        self.listbox_functions.bind("<FocusOut>", lambda x: self.listbox_function_contextmenu.unpost(), add='+')
        self.listbox_function_contextmenu.grab_release()




    def append_Function(self, fun, widget, event):
        if widget == event.widget:
            self.functionList.append(fun)
            self.update_window()

#   funktions eingabe
    def open_function_entry(self, term_type: fun.TermType, grad=0):
        fun_entry_win = funent.FunctionEntry(term_type, grad=grad)
        fun_entry_win.root.bind("<Destroy>", lambda x: self.append_Function(fun_entry_win.func, fun_entry_win.root, x))
        fun_entry_win.root.mainloop()
        self.functionList.append(fun_entry_win.func)

    def change_function_parameters_entry(self, event, funent):
        if event.widget == funent.root:
            print("change_function")
            self.functionList[self.selected_index] = funent.func
            self.selected_function = funent.func
            print("self.functionlist[self.selected_index]", self.functionList[self.selected_index])
            self.update_window()

    def change_function_parameters_ent(self):
        if self.selected_function.termtype == fun.TermType.GANZ_RATIONAL:
            func_entry = funent.FunctionEntry(self.selected_function.termtype, self.selected_function.term.original,
                                              grad=len(self.selected_function.term.original) - 1)
        else:
            func_entry = funent.FunctionEntry(self.selected_function.termtype, self.selected_function.term.original)
        func_entry.root.bind("<Destroy>", lambda e: self.change_function_parameters_entry(e, func_entry), add='+')
        func_entry.root.mainloop()

    def change_function_scalebar(self):
        sfc.ScalebarFunctionChangeWindow(self.update_window,
                                        self.selected_function,
                                        self.selected_index)

    def remove_function(self):
        self.functionList.remove(self.selected_function)
        self.selected_function = None
        self.selected_index = None
        self.update_window()

    def show_integral_result(self, lim1_str, lim2_str):
        try:
            lim1 = float(lim1_str)
            lim2 = float(lim2_str)
        except Exception as ex:
            raise
        integral = self.selected_function.calc_integral(lim1, lim2)
        msgbox.showinfo('Integral',
                        f"Integral von {self.selected_function} "
                        f"| lim{fun.subscript_of(1)}={lim1_str} "
                        f"| lim{fun.subscript_of(2)}={lim2_str} "
                        f" ist {fun.fun_round(integral, 3)}LE{fun.superscript_of(2)}")


    def open_integral_calc(self):
        root = tk.Toplevel()

        button = tk.Button(root, text='Eingeben')
        button.pack(side='bottom')

        label = tk.Label(root, text='unteres Limmit:')
        label.pack(side='left')

        lim1_entry_var = tk.StringVar()
        entry_lim1 = tk.Entry(root, textvariable=lim1_entry_var)
        entry_lim1.pack(side='left')

        label = tk.Label(root, text='oberes Limmit:')
        label.pack(side='left')

        lim2_entry_var = tk.StringVar()
        entry_lim2 = tk.Entry(root, textvariable=lim2_entry_var)
        entry_lim2.pack(side='left')

        button.config(command=lambda: self.show_integral_result(entry_lim1.get(), entry_lim2.get()))


    def rational_function_button_event(self, root:tk.Toplevel,  termType:fun.TermType, grad):
        root.destroy()
        self.open_function_entry(termType, grad)

    def rational_function(self):
        root = tk.Toplevel()
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

