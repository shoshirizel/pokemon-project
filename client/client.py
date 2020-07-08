import tkinter as tk
import requests
import tkinter.ttk  as ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.quit = None
        self.show_pokemons_button = None
        self.pokemon_button = None
        self.menu_button = None
        self.login_window = None
        self.master = master
        self.master.winfo_toplevel().title("Pokemon")
        self.pack()
        self.login()


    def create_widgets(self):
        if self.show_pokemons_button is None:
            self.show_pokemons_button = tk.Button(self.master)
            self.show_pokemons_button["text"] = "show pokemons"
            self.show_pokemons_button["command"] = self.show_pokemons
            self.show_pokemons_button.pack(side="top")

        self.create_evolve_button()

        if self.quit is None:
            self.quit = tk.Button(self, text="QUIT", fg="red",
                                command=self.master.destroy)
            self.quit.pack(side="bottom")

    def show_pokemons(self):
        if self.show_pokemons_button is not None:
            self.show_pokemons_button.destroy()
            self.show_pokemons_button = None
        
        if self.pokemon_button is not None:
           self.pokemon_button.destroy() 
           self.pokemon_button = None

        self.create_menu_button()
        res = requests.get(url=f'http://localhost:3000/pokemons?owner={self.name}')
        self.print_pokemons(res.json())



    def create_menu_button(self):
        if self.menu_button is not None:
            self.menu_button = tk.Button(self.master)
            self.menu_button["text"] = "Menu"
            self.menu_button["command"] = self.create_widgets
            self.menu_button.pack()


    def print(self, output):
        self.label = tk.Label(self, text= output)
        self.label.pack() 

    def print_pokemons(self, pkemons):
        for i, p in enumerate(pkemons["The pokemons"]):
            exec('Label%d=tk.Label(root,text="%s")\nLabel%d.pack()' % (i,p,i))

    def login(self):
        self.login_button = tk.Button(self)
        self.login_button["text"] = "Login"
        self.login_button["command"] = lambda: self.open_login_window()
        self.login_button.pack(pady = 10)


    def menu(self, name):
        if self.login_window is not None:
            self.login_window.destroy()
            self.login_window = None

        if self.login_button is not None:
            self.login_button.destroy()
            self.login_button = None
        
        self.name = name
        
        if self.valid_owner():
            self.create_widgets()
        else:
            self.open_login_window()

    def valid_owner(self):
        res = requests.get(url=f'http://localhost:3000/owners/{self.name}')
        if not res.status_code == 202:
            self.print("Invalid user.")
            return False
        return True
        


    def open_login_window(self): 
        self.login_window = tk.Toplevel(self.master) 
        self.login_window.title("Login") 
        self.login_window.geometry("200x200") 
        ttk.Label(self.login_window).pack() 
        login_lable = tk.Label(self.login_window, text="Owner Name")
        login_lable.pack(side = 'top')
        owner = tk.Entry(self.login_window, bd=5)
        owner.pack(side = 'top') 

        submit_button = tk.Button(self.login_window)
        submit_button["text"] = "Submit"
        submit_button["command"] = lambda: self.menu(owner.get())
        submit_button.pack(pady = 10)


    def enter_pokemon_to_ivolve(self):
        self.enter_pokemon = tk.Label(self, text="Enter a pokemon to ivolve")
        self.enter_pokemon.pack(side = 'top')
        self.pokemon = tk.Entry(self, bd =5)
        self.pokemon.pack(side = 'top')
        self.enter_pokemon_button = tk.Button(self)
        self.enter_pokemon_button["text"] = "Submit"
        self.enter_pokemon_button["command"] = self.evolve_pokemon
        self.enter_pokemon_button.pack(side="top")
        

    def evolve_pokemon(self):
        if self.show_pokemons_button is not None:
            self.show_pokemons_button.destroy()
            self.show_pokemons_button = None
        
        if self.pokemon_button is not None:
           self.pokemon_button.destroy() 
           self.pokemon_button = None

        self.create_menu_button()
           
        self.ivolve_pokemon = self.pokemon.get()
        res = requests.put(url=f"http://localhost:3000/evolve/{self.name}/{self.ivolve_pokemon}")
        self.print(res.json())



    def create_evolve_button(self):
        if self.pokemon_button is None:
            self.pokemon_button = tk.Button(self)
            self.pokemon_button["text"] = "Evolve pokemon"
            self.pokemon_button["command"] = self.enter_pokemon_to_ivolve
            self.pokemon_button.pack(side="top")



root = tk.Tk()
root.geometry("600x600")
app = Application(master=root)

app.mainloop()