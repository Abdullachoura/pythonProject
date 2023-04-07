import tkinter as tk
import types
import function as fun


class ScalebarFunctionChangeWindow:

    def __init__(self, update_win : types.FunctionType, selected_func : fun.Function, func_ind : int):
        self.update_win = update_win
        self.func = selected_func
        root = tk.Toplevel()
        label = tk.Label(root, text=f"{chr(ord('f') + func_ind)}={selected_func}")
        label.pack(side='top')
        self.entry_val_min_list = []
        self.entry_val_max_list = []
        self.scale_val_list = []
        self.entry_min_list = []
        self.entry_max_list = []
        self.scale_list = []
        if self.func.termtype == fun.TermType.GANZ_RATIONAL:
            len_orginal = len(selected_func.term.original)
            for i in range(len_orginal):
                scaleframe = ScalebarFrame(root, f"{chr(ord('a') + len_orginal - 1 - i)}", selected_func, i, update_win)
                scaleframe.pack(side='bottom')
                '''
                frame = tk.Frame(root)
                frame.pack(side='bottom')
                label = tk.Label(frame, text=f"{chr(ord('a') + len_orginal - 1 - i)}")
                label.pack(side='top')
                frame = tk.Frame(frame)
                frame.pack(side='bottom')

                scale_val = tk.DoubleVar()
                self.scale_val_list.append(scale_val)
                entry_val_min = tk.StringVar()
                self.entry_val_min_list.append(entry_val_min)
                entry_val_max = tk.StringVar()
                self.entry_val_max_list.append(entry_val_max)

                scale_val.set(selected_func.term.original[i])
                entry_val_min.set(str(-2 * abs(scale_val.get())))
                entry_val_max.set(str(2 * abs(scale_val.get())))

                entry_min = tk.Entry(frame, width=5, textvariable=entry_val_min)
                entry_min.pack(side='left')
                self.entry_min_list.append(entry_min)
                scalebar = tk.Scale(frame, from_=-2 * abs(scale_val.get()), to=2 * abs(scale_val.get()), variable=scale_val, orient=tk.HORIZONTAL)
                scalebar.pack(side='left')
                self.scale_list.append(scalebar)
                entry_max = tk.Entry(frame, width=5, textvariable=entry_val_max)
                entry_max.pack(side='left')
                self.entry_max_list.append(entry_max)
                '''
        elif self.func.termtype == fun.TermType.TRIGONOMETRISCH:
            frame = tk.Frame(root)
            label = tk.Label(frame, text=f"a")
            label.pack(side='top')
            frame = tk.Frame(frame)
            frame.pack(side='bottom')

            scale_val = tk.DoubleVar()
            self.scale_val_list.append(scale_val)
            entry_val_min = tk.StringVar()
            self.entry_val_min_list.append(entry_val_min)
            entry_val_max = tk.StringVar()
            self.entry_val_max_list.append(entry_val_max)

            scale_val.set(selected_func.term.original[0])
            entry_val_min.set(str(-2 * abs(scale_val.get())))
            entry_val_max.set(str(2 * abs(scale_val.get())))

            entry_min = tk.Entry(frame, width=5, textvariable=entry_val_min)
            entry_min.pack(side='left')
            self.entry_min_list.append(entry_min)
            scalebar = tk.Scale(frame, from_=-2 * abs(scale_val.get()), to=2 * abs(scale_val.get()), variable=scale_val,
                                orient=tk.HORIZONTAL)
            scalebar.pack(side='left')
            self.scale_list.append(scalebar)
            entry_max = tk.Entry(frame, width=5, textvariable=entry_val_max)
            entry_max.pack(side='left')
            self.entry_max_list.append(entry_max)

            frame = tk.Frame(root)
            label = tk.Label(frame, text=f"{chr(0x03D5)}")
            label.pack(side='top')
            frame = tk.Frame(frame)
            frame.pack(side='bottom')

            scale_val = tk.DoubleVar()
            self.scale_val_list.append(scale_val)
            entry_val_min = tk.StringVar()
            self.entry_val_min_list.append(entry_val_min)
            entry_val_max = tk.StringVar()
            self.entry_val_max_list.append(entry_val_max)

            scale_val.set(selected_func.term.original[1])
            entry_val_min.set(str(-2 * abs(scale_val.get())))
            entry_val_max.set(str(2 * abs(scale_val.get())))

            entry_min = tk.Entry(frame, width=5, textvariable=entry_val_min)
            entry_min.pack(side='left')
            self.entry_min_list.append(entry_min)
            scalebar = tk.Scale(frame, from_=-2 * abs(scale_val.get()), to=2 * abs(scale_val.get()), variable=scale_val,
                                orient=tk.HORIZONTAL)
            scalebar.pack(side='left')
            self.scale_list.append(scalebar)
            entry_max = tk.Entry(frame, width=5, textvariable=entry_val_max)
            entry_max.pack(side='left')
            self.entry_max_list.append(entry_max)

            frame = tk.Frame(root)
            label = tk.Label(frame, text=f"w")
            label.pack(side='top')
            frame = tk.Frame(frame)
            frame.pack(side='bottom')

            scale_val = tk.DoubleVar()
            self.scale_val_list.append(scale_val)
            entry_val_min = tk.StringVar()
            self.entry_val_min_list.append(entry_val_min)
            entry_val_max = tk.StringVar()
            self.entry_val_max_list.append(entry_val_max)

            scale_val.set(selected_func.term.original[0])
            entry_val_min.set(str(-2 * abs(scale_val.get())))
            entry_val_max.set(str(2 * abs(scale_val.get())))

            entry_min = tk.Entry(frame, width=5, textvariable=entry_val_min)
            entry_min.pack(side='left')
            scalebar = tk.Scale(frame, from_=-2 * abs(scale_val.get()), to=2 * abs(scale_val.get()), variable=scale_val,
                                orient=tk.HORIZONTAL)
            scalebar.pack(side='left')
            entry_max = tk.Entry(frame, width=5, textvariable=entry_val_max)
            entry_max.pack(side='left')
        else:
            for i in range(len(self.func.term.original)):
                frame = tk.Frame(root)
                frame.pack(side="top")
                label = tk.Label(frame, text=f"{chr(ord('a') + i)}")
                label.pack(side='top')
                frame = tk.Frame(frame)
                frame.pack(side='bottom')

                scale_val = tk.DoubleVar()
                self.scale_val_list.append(scale_val)
                entry_val_min = tk.StringVar()
                self.entry_val_min_list.append(entry_val_min)
                entry_val_max = tk.StringVar()
                self.entry_val_max_list.append(entry_val_max)

                entry_min = tk.Entry(frame, width=5, textvariable=entry_val_min)
                entry_min.pack(side='left')
                scalebar = tk.Scale(frame, from_=-2 * abs(scale_val.get()), to=2 * abs(scale_val.get()), variable=scale_val, orient=tk.HORIZONTAL)
                scalebar.pack(side='left')
                entry_max = tk.Entry(frame, width=5, textvariable=entry_val_max)
                entry_max.pack(side='left')

                scale_val.set(selected_func.term.original[i])
                entry_val_min.set(str(-2 * abs(scale_val.get())))
                entry_val_max.set(str(2 * abs(scale_val.get())))
        for i in range(len(self.entry_max_list)):
            self.entry_val_max_list[i].trace_add('write',
                                                 lambda var, ind, y: self.change_min_val(self.entry_max_list[i],
                                                                                         self.scale_list[i]))
            self.entry_val_min_list[i].trace_add('write',
                                                 lambda var, ind, y: self.change_max_val(self.entry_min_list[i],
                                                                                         self.scale_list[i]))
            self.scale_val_list[i].trace_add("write", lambda var, ind, y: self.change_factor(var))

    def change_min_val(self, var, scalebar):
        try:
            min_val = float(var)
            scalebar.config(from_=min_val)
        except:
            pass

    def change_max_val(self, var, scalebar):
        try:
            max_val = float(var)
            scalebar.config(to=max_val)
        except:
            pass

    def change_factor(self, var):
        index = self.scale_val_list.index(var)
        self.func.term.original[index] = self.scale_val_list[index].get()
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
