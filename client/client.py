import tkinter as tk
import requests

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.login()


    def create_widgets(self):
        self.show_pokemons_button = tk.Button(self)
        self.show_pokemons_button["text"] = "show pokemons"
        self.show_pokemons_button["command"] = self.show_pokemons
        self.show_pokemons_button.pack(side="top")


        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def show_pokemons(self):
        self.show_pokemons_button.destroy()
        self.login_lable.destroy()
        self.owner.destroy()
        res = requests.get(url=f'http://localhost:3000/pokemons?owner={self.name}')
        self.print(res.json())


    def print(self, output):
        self.label = tk.Label(self, text= output)
        self.label.pack() 

    def login(self):
        self.login_lable = tk.Label(self, text="Owner Name")
        self.login_lable.pack(side = 'top')
        self.owner = tk.Entry(self, bd=5)
        self.owner.pack(side = 'top') 

        self.login_button = tk.Button(self)
        self.login_button["text"] = "Login"
        self.login_button["command"] = self.menu
        self.login_button.pack(side="top")

    def menu(self):
        self.name = self.owner.get()
        self.valid_owner()
        self.login_lable.destroy()
        self.login_button.destroy()
        self.create_widgets()

    def valid_owner(self):
        res = requests.get(url=f'http://localhost:3000/owners/{self.name}')
        if not res.status_code == 202:
            self.print("Invalid user.")
            self.login_lable.destroy()
            self.owner.destroy()
            self.login()




root = tk.Tk()
app = Application(master=root)
app.mainloop()