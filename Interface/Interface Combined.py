import tkinter as tk
from IPython.display import display
import ipyleaflet as ipy

class WelcomePage(tk.Frame):
    def __init__(self, master, next_callback):
        super().__init__(master)
        self.next_callback = next_callback
        tk.Label(self, text="Welcome to my app!").pack()
        tk.Button(self, text="Next", command=self.next_callback).pack()

class MapPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.map = ipy.Map(center=[37.7749,-122.4194], zoom=10)
        display(self.map)
        tk.Button(self, text="Back", command=self.back_callback).pack()

    def back_callback(self):
        self.master.show_welcome_page()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.geometry("400x300")
        self.welcome_page = WelcomePage(self, self.show_map_page)
        self.map_page = MapPage(self)
        self.show_welcome_page()

    def show_welcome_page(self):
        self.map_page.pack_forget()
        self.welcome_page.pack()

    def show_map_page(self):
        self.welcome_page.pack_forget()
        self.map_page.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
