import tkinter
import tkinter as tk
import tkinter.messagebox as msgbox
from Function import Function
from Function import TermType


class FunctionEntry:

    entry_arr : []
    func : Function

    def __init__(self, term_type, grad):
        self.root = tk.Tk()
        self.entry_arr = []
        self.termType = term_type

        frame = tk.Frame(self.root)
        frame.pack(side='top')

        button = tk.Button(self.root, text='eingeben', command=self.enter_function)
        button.pack(side='bottom')
        if term_type == TermType.GANZ_RATIONAL:
            for i in range(grad+1):
                if i==0:
                    text = tk.Entry(frame, width=5)
                    text.pack(side='right')
                    self.entry_arr.append(text)
                    continue
                if i==1:
                    label_str = 'x'
                else:
                    label_str = 'x^{0}'.format(str(i))
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
                if i == len(self.entry_arr)-1:
                    factor = self.convert_factor_entry(self.entry_arr[i].get(), False)
                else:
                    factor = self.convert_factor_entry(self.entry_arr[i].get(), True)
                func_factors.append(factor)
            self.func = Function(self.termType, *func_factors)
            self.root.destroy()
        except ValueError as e:
            msgbox.showinfo('Falsche Eingabe', e.args[0])

