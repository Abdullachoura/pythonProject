import tkinter as tk
import types
import function as fun


class ScalebarFunctionChangeWindow:

    def __init__(self, update_win, selected_func: fun.Function, func_ind: int):
        self.update_win = update_win
        self.func = selected_func
        self.func_ind = func_ind
        root = tk.Toplevel()
        self.label = tk.Label(root, text=f"{chr(ord('f') + func_ind)}={selected_func}")
        self.label.pack(side='top')
        if self.func.termtype == fun.TermType.GANZ_RATIONAL:
            len_orginal = len(selected_func.term.original)
            for i in range(len_orginal):
                scaleframe = ScalebarFrame(root, f"{chr(ord('a') + len_orginal - 1 - i)}", selected_func, i, self.update_funktion)
                scaleframe.pack(side='bottom')
        elif self.func.termtype == fun.TermType.TRIGONOMETRISCH:
            scaleframe = ScalebarFrame(root, f"a", selected_func, 0, self.update_funktion)
            scaleframe.pack(side='top')
            scaleframe = ScalebarFrame(root, chr(0x03C6), selected_func, 1, self.update_funktion)
            scaleframe.pack(side='top')
            scaleframe = ScalebarFrame(root, "w", selected_func, 2, self.update_funktion)
            scaleframe.pack(side='top')
        else:
            for i in range(len(self.func.term.original)):
                scalebar_frame = ScalebarFrame(root, chr(ord('a') + i), selected_func, i, self.update_funktion)
                scalebar_frame.pack(side='top')

    def update_funktion(self):
        self.label.config(text=f"{chr(ord('f') + self.func_ind)}={self.func}")
        self.update_win()

class ScalebarFrame(tk.Frame):

    def __init__(self, master, label, selected_func, index, callback):
        super().__init__(master)
        self.selected_func = selected_func
        self.index = index
        self.callback = callback
        frame = tk.Frame(self)
        frame.pack(side='bottom')
        label = tk.Label(frame, text=label)
        label.pack(side='top')
        frame = tk.Frame(frame)
        frame.pack(side='bottom')

        self.scale_val = tk.DoubleVar()
        self.entry_val_min = tk.StringVar()
        self.entry_val_max = tk.StringVar()

        self.scale_val.set(selected_func.term.original[index])
        self.entry_val_min.set(str(-2 * abs(self.scale_val.get())))
        self.entry_val_max.set(str(2 * abs(self.scale_val.get())))

        entry_min = tk.Entry(frame, width=5, textvariable=self.entry_val_min)
        entry_min.pack(side='left')
        self.scalebar = tk.Scale(frame, from_=-2 * abs(self.scale_val.get()), to=2 * abs(self.scale_val.get()),
                            variable=self.scale_val, orient=tk.HORIZONTAL)
        self.scalebar.pack(side='left')
        entry_max = tk.Entry(frame, width=5, textvariable=self.entry_val_max)
        entry_max.pack(side='left')
        self.entry_val_max.trace_add('write',
                                             lambda var, ind, y: self.change_max_val())
        self.entry_val_min.trace_add('write',
                                             lambda var, ind, y: self.change_min_val())
        self.scale_val.trace_add("write", lambda var, ind, y: self.change_factor(index))

    def change_min_val(self):
        try:
            fromval = float(self.entry_val_min.get())
            self.scalebar.config(from_=fromval)
        except:
            pass

    def change_max_val(self):
        try:
            toval = float(self.entry_val_max.get())
            self.scalebar.config(to=toval)
        except:
            pass

    def change_factor(self, index):
        self.selected_func.term.original[index] = self.scale_val.get()
        self.callback()
