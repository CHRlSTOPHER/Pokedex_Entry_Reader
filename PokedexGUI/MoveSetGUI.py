import tkinter as tk
import ttkbootstrap as tb

HEIGHT = 18
WIDTH = 48


class MoveSetGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text=" Move Set ", width=WIDTH, height=HEIGHT,
                         style='frame.TLabelframe', labelanchor='n',)
        self.grid(column=0, row=1, pady=(2, 4), rowspan=5)
        self.generate()

    def generate(self):
        self.list_box = tk.Listbox(self, width=WIDTH, height=HEIGHT)
        self.list_box.grid(pady=(2, 8), padx=9)
