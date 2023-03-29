import time
import tkinter
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk

from Function import Function
from Function import TermType
from Function import superscript_of
from Function import TrigonometrischerOperator as TriOp


class FunctionEntry:

    entry_arr : []
    func : Function

    def __init__(self, term_type, *args):
        self.root = tk.Tk()
        self.entry_arr = []
        self.termType = term_type

        frame = tk.Frame(self.root)
        frame.pack(side='top')

        button = tk.Button(self.root, text='eingeben', command=self.enter_function)
        button.pack(side='bottom')
        if term_type == TermType.GANZ_RATIONAL:
            for i in range(args[0]+1):
                if i==0:
                    text = tk.Entry(frame, width=5)
                    text.pack(side='right')
                    self.entry_arr.append(text)
                    continue
                if i==1:
                    label_str = 'x'
                else:
                    label_str = f'x{superscript_of(i)}'
                label = tk.Label(frame, text=label_str)
                label.pack(side='right')
                text = tk.Entry(frame, width=5)
                text.pack(side='right')
                self.entry_arr.append(text)

        elif term_type == TermType.SCHNITTPUNKT:
            text = tk.Entry(frame, width=5)
            text.pack(side='left')
            self.entry_arr.append(text)
            label = tk.Label(frame, text="(x")
            label.pack(side='left')
            text = tk.Entry(frame, width=5)
            text.pack(side='left')
            self.entry_arr.append(text)
            label = tk.Label(frame, text=")²")
            label.pack(side='left')
            text = tk.Entry(frame, width=5)
            text.pack(side='left')
            self.entry_arr.append(text)

        elif term_type == TermType.TRIGONOMETRISCH:
            text = tk.Entry(frame, width=5)
            text.pack(side='left')
            self.entry_arr.append(text)

            label = tk.Label(frame, text='*')
            label.pack(side='left')

            self.comboBox = ttk.Combobox(frame, values=['sin', 'cos'], state='readonly')
            self.comboBox.set('sin')
            self.comboBox.pack(side='left')

            label = tk.Label(frame, text=f'({chr(0x03c9)}t')
            label.pack(side='left')

            text = tk.Entry(frame, width=5)
            text.pack(side='left')
            self.entry_arr.append(text)

            label = tk.Label(frame, text=') | T=')
            label.pack(side='left')

            entry = tk.Entry(frame, width=5)
            entry.pack(side='left')
            self.entry_arr.append(entry)






    def convert_factor_entry(self, factor: str, sign_needed: bool) -> float:
        if len(factor) == 0:
            raise ValueError("Alle Eingabefelder sollten ausgefüllt sein")
        elif factor[0] == '+':
            to_return = float(factor[1:])
            return to_return
        elif factor[0] == '-':
            to_return = -1 * float(factor[1:])
            return to_return
        elif not sign_needed:
            to_return = float(factor)
            return to_return
        elif factor[0].isdigit():
            raise ValueError("Vorzeichen erwartet. + oder - an erster Stelle eingeben")
        else:
            raise ValueError("Vorzeichen ungültig. + oder - an erster Stelle eingeben eingeben.")


    def enter_function(self):
        try:
            func_factors = []
            for i in range(len(self.entry_arr)):
                if i == len(self.entry_arr)-1 and self.termType.GANZ_RATIONAL:
                    factor = self.convert_factor_entry(self.entry_arr[i].get(), False)
                elif i == 0:
                    factor = self.convert_factor_entry(self.entry_arr[i].get(), False)
                else:
                    factor = self.convert_factor_entry(self.entry_arr[i].get(), True)
                func_factors.append(factor)
            if self.termType == TermType.TRIGONOMETRISCH:
                if self.comboBox.get() == 'sin':
                    trigOp = TriOp.SIN
                elif self.comboBox.get() == 'cos':
                    trigOp = TriOp.COS
                self.func = Function(self.termType, trigOp, *func_factors)
            else:
                self.func = Function(self.termType, *func_factors)
            time.sleep(0.005)
            self.root.destroy()
        except ValueError as e:
            msgbox.showinfo('Falsche Eingabe', e.args[0])

