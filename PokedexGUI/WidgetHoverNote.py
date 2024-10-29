from tkinter import Toplevel, Label, LEFT, SOLID

X_SPACING = 42
Y_SPACING = 20


class WidgetHoverNote(Toplevel):

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.label = None

        self.generate()

    def generate(self):
        def enter(event):
            self.create_note()
        def leave(event):
            self.destroy_note()

        self.widget.bind('<Enter>', enter)
        self.widget.bind('<Leave>', leave)

    def create_note(self):
        super().__init__(self.widget)

        self.label = Label(self, text=self.text, justify=LEFT,
                           background="#ffffe0", relief=SOLID, borderwidth=1,
                           font=("tahoma", 10, "normal"))
        self.label.pack(ipadx=1)

        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + X_SPACING
        y = y + cy + self.widget.winfo_rooty() + Y_SPACING
        self.wm_overrideredirect(1)
        self.wm_geometry("+%d+%d" % (x, y))

    def destroy_note(self):
        self.destroy()

    def cleanup(self):
        self.destroy()
        self = None
