import tkinter as tk
import loginWindow
import database

database.databaseStartup()

loginWindow.LoginWindow()



'''
root = tk.Tk()
root.minsize(width=1000, height=1000)
root.maxsize(width=True, height=True)
root.resizable(width=True, height=True)
root.title("Anmeldefenster")
label1 = tk.Label(root, text="Herzlich willkommen", bg="orange")
label1.pack()


def label1Aendern():
 label1["text"] = "Aufwiedersehen"

schaltf1 = tk.Button(root, text="Aktion durchführen", command=label1Aendern)
schaltf1.pack()

schaltf1 = tk.Button(root, text= "fenster schliessen")
schaltf2 = tk.Button(root, text= "beenden", command=root.quit)
schaltf2.pack()
'''













root.mainloop()