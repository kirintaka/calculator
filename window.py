import tkinter as tk
from tkinter import font
from decimal import Decimal, getcontext
from tkinter import messagebox
import pyperclip

class Window(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.master = master
    
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size = 20)
    
    getcontext().prec = 30
  
    menu = tk.Menu(self.master)
    self.master.config(menu=menu)
  
    self.master.bind('<Control-c>', self.copy)
    self.master.bind('<Control-C>', self.copy)
    
    aboutMenu = tk.Menu(menu)
    aboutMenu.add_command(label='about', command=self.showAbout)
    menu.add_cascade(label="about", menu=aboutMenu)

    fileMenu = tk.Menu(menu)
    fileMenu.add_command(label="Exit", command=self.exitProgram)
    menu.add_cascade(label="exit", menu=fileMenu)
    
    self.first = tk.Text(master, height=1, width=20, font=('Arial', 16))
    self.first.bind('<Control-V>', lambda text=self.first: self.paste(text))
    self.first.grid(columnspan=20, row=0, column=0)
    self.second = tk.Text(master, height=1, width=20, font=('Arial', 16))
    self.second.bind('<Control-V>', lambda text=self.second: self.paste(text))
    self.second.grid(columnspan=20, row=0, column=20)
    self.result = tk.Text(master, height=1, width=20, font=('Arial', 16))
    self.result.grid(columnspan=20, row=1, column=0)
        
    self.plusButton = tk.Button(master, text="+", command=self.plus)
    self.plusButton.grid(row=3, column=0, rowspan=1)
    
    self.minusButton = tk.Button(master, text="-", command=self.minus)
    self.minusButton.grid(row=3, column=1, rowspan=1)
    
    self.multButton = tk.Button(master, text="*", command=self.mult)
    self.multButton.grid(row=3, column=2, rowspan=1)
    
    self.divButton = tk.Button(master, text="*", command=self.divide)
    self.divButton.grid(row=3, column=3, rowspan=1)
  
  def plus(self):
    try:
      first = self.first.get(1.0, 'end').replace(',', '.')
      second = self.second.get(1.0, 'end').replace(',', '.')
      if self.check_result(Decimal(first)) or self.check_result(Decimal(second)):
        messagebox.showerror('Ошибка', 'Число превышает допустимое значение.')
        return
      if 'e' in first or 'e' in second:
        messagebox.showerror('Ошибка', 'Вы не можете использовать числа в экспоненциальной нотации.')
        return
      result = Decimal(first) + Decimal(second)
      if self.check_result(result):
        messagebox.showerror('Ошибка', 'Результат превышает допустимое значение.')
        return
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, "{:.6f}".format(result))
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'error in plus')
      
  def minus(self):
    try:
      first = self.first.get(1.0, 'end').replace(',', '.')
      second = self.second.get(1.0, 'end').replace(',', '.')
      if self.check_result(Decimal(first)) or self.check_result(Decimal(second)):
        messagebox.showerror('Ошибка', 'Число превышает допустимое значение.')
        return
      if 'e' in first or 'e' in second:
        messagebox.showerror('Ошибка', 'Вы не можете использовать числа в экспоненциальной нотации.')
        return
      result = Decimal(first) - Decimal(second)
      if self.check_result(result):
        messagebox.showerror('Ошибка', 'Результат превышает допустимое значение.')
        return   
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, "{:.6f}".format(result))
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'error in minus')
    
  def mult(self):
    try:
      first = self.first.get(1.0, 'end').replace(',', '.')
      second = self.second.get(1.0, 'end').replace(',', '.')
      if self.check_result(Decimal(first)) or self.check_result(Decimal(second)):
        messagebox.showerror('Ошибка', 'Число превышает допустимое значение.')
        return
      if 'e' in first or 'e' in second:
        messagebox.showerror('Ошибка', 'Вы не можете использовать числа в экспоненциальной нотации.')
        return
      result = Decimal(first) * Decimal(second)
      if self.check_result(result):
        messagebox.showerror('Ошибка', 'Результат превышает допустимое значение.')
        return
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, "{:.6f}".format(result))
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'error in plus')
  
  def divide(self):
    try:
      first = self.first.get(1.0, 'end').replace(',', '.')
      second = self.second.get(1.0, 'end').replace(',', '.')
      if self.check_result(Decimal(first)) or self.check_result(Decimal(second)):
        messagebox.showerror('Ошибка', 'Число превышает допустимое значение.')
        return
      if 'e' in first or 'e' in second:
        messagebox.showerror('Ошибка', 'Вы не можете использовать числа в экспоненциальной нотации.')
        return
      result = Decimal(first) / Decimal(second)
      if self.check_result(result):
        messagebox.showerror('Ошибка', 'Результат превышает допустимое значение.')
        return
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, "{:.6f}".format(result))
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'error in plus')
  
  def copy(self, event=None):
    self.clipboard_clear()
    self.update()
    pyperclip.copy(self.selection_get())
    self.update()
    return 'break'
  
  def paste(self, text, event=None):
    text.insert(1.0, pyperclip.paste())
    self.clipboard_clear()
    self.update()
    return 'break'
  
  def check_result(self, result):
    min_value = Decimal(-1000000000000.000000)
    max_value = Decimal(1000000000000.000000)
    return result < min_value or result > max_value
  
  def exitProgram(self):
    exit()
  
  def showAbout(self):
    messagebox.showinfo('About', 'Жалова Дарья Александровна\n4 курс 4 группа\n2023')
  
    