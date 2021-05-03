import tkinter as tk

class EmpthUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.master.title('Hello world')

        self.c = tk.Canvas(self, width = 480, height = 240, highlightthickness = 0)
        self.c.create_text(10, 200, text='Hello World', font='courier 20', anchor = tk.SW)
        self.c.pack()

f = EmpthUI()
f.pack()
f.mainloop()