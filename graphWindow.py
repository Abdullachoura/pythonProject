import tkinter
import tkinter as tk

class GraphWindow:

    functionList: []




    def __init__(self):
        root = tk.Tk()
        root.title('Functional')
        self.functionList = []

        menubar = tk.Menu(root)
        root.config(menu=menubar)
        menu = tk.Menu(menubar)
        menu.add_cascade(
            label='Neue Funktion',
            menu=menu
        )

        listboxFunctions = tkinter.Listbox(root, listvariable=self.functionList, width=50)
        listboxFunctions.pack(side="left", fill='y')

        root.mainloop()