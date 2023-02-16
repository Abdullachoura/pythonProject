import tkinter as tk
import tkinter.messagebox as msgbox
import database as db

class LoginWindow:

    name: tk.StringVar
    password: tk.StringVar
    root: tk.Tk

    def __init__(self):
        self.root = tk.Tk()
        self.name = tk.StringVar()
        self.password = tk.StringVar()
        self.root.title = 'Login/Register'
        self.root.eval('tk::PlaceWindow . center')

        labelUsername = tk.Label(self.root, text='Nutzer')
        labelUsername.pack(side='top')

        enterUsername = tk.Entry(self.root, textvariable=self.name)
        enterUsername.pack(side='top', fill="x")

        labelPassword = tk.Label(self.root, text='Passwort')
        labelPassword.pack(side='top')

        enterPassword = tk.Entry(self.root,show='*', textvariable=self.password)
        enterPassword.pack(side='top')

        buttonRegister = tk.Button(self.root, text='registrieren', command=self.register)
        buttonRegister.pack(side='top', fill="both")

        buttonLogin = tk.Button(self.root, text='einloggen', command=self.login)
        buttonLogin.pack(side='top', fill='both')

        self.root.mainloop()

    def register(self):
        boolVar, message = db.register(self.name.get(), self.password.get())

        if boolVar:
            title = 'Erfolgreich Registriert'
        else:
            title = 'Registrierung fehlgeschlagen'

        msgbox.showinfo(title, message)


    def login(self):
        boolVar, message = db.login(self.name.get(), self.password.get())

        if boolVar:
            title = 'Erfolgreich Eingelogt'
        else:
            title = 'Einloggen fehlgeschlagen'

        msgbox.showinfo(title, message)
        self.root.destroy()




