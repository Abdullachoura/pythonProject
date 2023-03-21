import tkinter as tk
import loginWindow
import database
import graphWindow

'''
greeting = tk.Label(text="hello, mein friseur ist nice")
greeting.pack()
Label = tk.Label(text="hello, tkinter")
foreground = "white"
background = "black"
label = tk.Label(text="Hello, Tkinter", background="#34A2FE")
label = tk.Label(text="Hello, Tkinter", fg="white", bg="black")
label = tk.Label(
    text="Hello, Tkinter",
    fg="white",
    bg="black",
    width=10,
    height=10
)
button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow", command=root.quit
)
button.pack()
'''



database.databaseStartup()
loginWin = loginWindow.LoginWindow()
if (loginWin.logged_in == False): #remove == False
    graphWindow.GraphWindow()



'''
root = tk.Tk()
root.minsize(width=1000, height=1000)
root.maxsize(width=True, height=True)
root.resizable(width=True, height=True)
root.title("Anmeldefenster")
label1 = tk.Label(root, text="Herzlich willkommen", bg="orange")
label1.pack()
label1.place=()






def label1Aendern():
 label1["text"] = "Aufwiedersehen"

schaltf1 = tk.Button(root, text="Aktion durchführen", command=label1Aendern)
schaltf1.pack()

schaltf1 = tk.Button(root, text= "fenster schliessen")
schaltf2 = tk.Button(root, text= "beenden", command=root.quit)
schaltf2.pack()
root.mainloop()
'''
