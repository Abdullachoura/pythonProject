import tkinter as tk
import database as db

class Regestrierungsfenster:


    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Registrierungsfenster")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        username_label = tk.Label(self.root, text="Benutzername:")
        username_label.pack()
        username_entry = tk.Entry(self.root, textvariable=self.username_var)
        username_entry.pack()

        password_label = tk.Label(self.root, text="Passwort:")
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*", textvariable=self.password_var)
        password_entry.pack()

        submit_button = tk.Button(self.root, text="Registrieren",
                                  command=self.registrieren)
        submit_button.pack()

        self.root.mainloop()

    def registrieren(self):
        db.register(self.username_var.get(), self.password_var.get())
        self.root.destroy()



