import tkinter
import tkinter as tk
import tkinter.messagebox as msgbox
from function import Function


class FunctionEntry:

    entry_arr : []
    func : Function

    def __init__(self, grad):
        root = tk.Tk()
        self.entry_arr = []

        frame = tk.Frame(root)
        frame.pack(side='top')

        button = tk.Button(root)
        button.pack('bottom')

        for i in range(grad):
            if grad==0:
                text = tk.Entry(frame)
                text.pack(side='left')
                self.entry_arr.append(text)
                continue
            if grad==1:
                label_str = 'x'
            else:
                label_str = 'x^{0}'.format(str(i))
            label = tk.Label(frame, text=label_str)
            label.pack(side='right')
            text = tk.Entry(frame, width=10)
            text.pack(side='right')
            self.entry_arr.append(text)
        root.mainloop()

    def convert_factor_entry(self, factor: str) -> float:
        if factor[0] == '+':
            to_return = float(factor[1:])
            return to_return
        elif factor[0] == '-':
            to_return = -1 * float(factor[1:])
            return to_return
        elif factor[0].isdigit():
            raise ValueError("Vorzeichen erwartet. + oder - an erster Stelle eingeben")
        else:
            raise ValueError("Vorzeichen ungültig. + oder - an erster Stelle eingeben eingeben.")

    def enter_function(self):
        try:
            func_factors = []
            for entry in self.entry_arr:
                factor = self.convert_factor_entry(entry.get())
                func_factors.append(factor)
            self.func = Function(func_factors)
        except ValueError as e:
            msgbox.showinfo('Falsche Eingabe', e.args[0])
