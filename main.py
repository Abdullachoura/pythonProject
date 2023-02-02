import tkinter as tk

root = tk.Tk()
root.minsize(width=1000, height=1000)
root.maxsize(width=True, height=True)
root.resizable(width=True, height=True)
root.title("Anmeldefenster")
label1 = tk.Label(root, text="Herzlich willkommen")
label1.pack()

schaltf1 = tk.Button(root, text="aktion durchführen")
schaltf1.pack()








root.mainloop()