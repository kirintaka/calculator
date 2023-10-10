from tkinter import *
from window import Window

root = Tk()
app = Window(root)

# set window title
root.wm_title("Финансовый калькулятор")
root.geometry("500x400")

# show window
root.mainloop()

