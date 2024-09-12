from PokeApiDataManager import PokeApiDataManager

from tkinter import Tk
from tkinter import ttk as tk


poke_api_manager = PokeApiDataManager()

root = Tk()
frame = tk.Frame(root, padding=10)
frame.grid()

tk.Label(frame, text="Choose a Pokemon").grid(column=0, row=0)
dex_name_entry = tk.Entry(frame).grid(column=1, row=0, padx=5)
root.bind("<Return>", poke_api_manager.scrape_poki_api_data)


root.mainloop()