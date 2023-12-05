import tkinter as tk
from tkinter import font
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_HALF_EVEN
from tkinter import messagebox
from math import floor
import pyperclip
import re

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
    
    self.selected_option1 = tk.StringVar(master, "+")
    self.selected_option2 = tk.StringVar(master, "+")
    self.selected_option3 = tk.StringVar(master, "+")
    
    clmn = 0
    self.first = tk.Text(master, height=1, width=24, font=('Arial', 16))
    self.first.bind('<Control-V>', lambda text=self.first: self.paste(text))
    self.first.grid(columnspan=24, row=1, column=clmn)
    self.first.insert(1.0, "0")
    clmn += 24
    self.operaion1 = tk.OptionMenu(master, self.selected_option1, "+", "-", "*", "/")
    self.operaion1.grid(columnspan=2 ,row=1, column=clmn)
    clmn += 2
    self.right = tk.Label(master, height=1, width=2, font=('Arial', 16), text='(')
    self.right.grid(columnspan=2, row=1, column=clmn)
    clmn += 2
    self.second = tk.Text(master, height=1, width=24, font=('Arial', 16))
    self.second.bind('<Control-V>', lambda text=self.second: self.paste(text))
    self.second.grid(columnspan=24, row=1, column=clmn)
    self.second.insert(1.0, "0")
    clmn += 24
    self.operaion2 = tk.OptionMenu(master, self.selected_option2, "+", "-", "*", "/")
    self.operaion2.grid(columnspan=2, row=1, column=clmn)
    clmn += 2
    self.third = tk.Text(master, height=1, width=24, font=('Arial', 16))
    self.third.bind('<Control-V>', lambda text=self.third: self.paste(text))
    self.third.grid(columnspan=24, row=1, column=clmn)
    self.third.insert(1.0, "0")
    clmn += 24
    self.left = tk.Label(master, height=1, width=2, font=('Arial', 16), text=')')
    self.left.grid(columnspan=2, row=1, column=clmn)
    clmn += 2
    self.operaion3 = tk.OptionMenu(master, self.selected_option3, "+", "-", "*", "/")
    self.operaion3.grid(columnspan=2, row=1, column=clmn)
    clmn += 2
    self.fourth = tk.Text(master, height=1, width=24, font=('Arial', 16))
    self.fourth.bind('<Control-V>', lambda text=self.fourth: self.paste(text))
    self.fourth.grid(columnspan=24, row=1, column=clmn)
    self.fourth.insert(1.0, "0")
    clmn += 24
    
    self.resultButton = tk.Button(master, text="=", command=self.get_result)
    self.resultButton.grid(row=3, column=clmn // 2, rowspan=1)
    
    self.resultLabel = tk.Label(master, height=1, width=24, font=('Arial', 16), text='Результат:')
    self.resultLabel.grid(columnspan=2, row=3, column=0)
    self.result = tk.Text(master, height=1, width=24, font=('Arial', 16))
    self.result.grid(columnspan=24, row=4, column=0)
    self.result.insert(1.0, "0")
    
    self.roundedLabel = tk.Label(master, height=1, width=24, font=('Arial', 16), text='Округление:')
    self.roundedLabel.grid(columnspan=2, row=6, column=0)
    clmn2 = 0
    self.mathButton = tk.Button(master, text="Математическое округление", command=self.round_math)
    self.mathButton.grid(columnspan=24, row=8, column=clmn2)
    clmn2 += 24
    self.bankButton = tk.Button(master, text="Банковское округление", command=self.round_bank)
    self.bankButton.grid(columnspan=24, row=8, column=clmn2)
    clmn2 += 24
    self.downButton = tk.Button(master, text="Усечение", command=self.round_down)
    self.downButton.grid(columnspan=24, row=8, column=clmn2)
    
    self.rounded = tk.Text(master, height=1, width=24, font=('Arial', 16))
    self.rounded.grid(columnspan=24, row=10, column=0)
    self.rounded.insert(1.0, "0")
    
  def round_math(self):
    number = Decimal(self.result.get(1.0, 'end').replace(',', '.').rstrip('\n'))
    result = number.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    self.rounded.delete(1.0, 'end')
    self.rounded.insert(1.0, self.format_answer(result))
  
  def round_bank(self):
    number = Decimal(self.result.get(1.0, 'end').replace(',', '.').rstrip('\n'))
    result = number.quantize(Decimal('1'), rounding=ROUND_HALF_EVEN)
    self.rounded.delete(1.0, 'end')
    self.rounded.insert(1.0, self.format_answer(result))
  
  def round_down(self):
    number = Decimal(self.result.get(1.0, 'end').replace(',', '.').rstrip('\n'))
    result = floor(number)
    self.rounded.delete(1.0, 'end')
    self.rounded.insert(1.0, self.format_answer(result))
  
  def __calculate(self, operation, a, b):
    if isinstance(a, str):
      a = Decimal(a.replace(' ', ''))
    if isinstance(b, str):
      b = Decimal(b.replace(' ', ''))
    if operation == "+":
      return self.plus(a, b)
    elif operation == "-":
      return self.minus(a, b)
    elif operation == "*":
      return self.mult(a, b)
    else:
      return self.divide(a, b)
    
  
  def get_result(self):
    try:
      first = self.first.get(1.0, 'end').replace(',', '.').rstrip('\n')
      second = self.second.get(1.0, 'end').replace(',', '.').rstrip('\n')
      third = self.third.get(1.0, 'end').replace(',', '.').rstrip('\n')
      fourth = self.fourth.get(1.0, 'end').replace(',', '.').rstrip('\n')
      if not (self.is_valid_number(first) and self.is_valid_number(second)
              and self.is_valid_number(third) and self.is_valid_number(fourth)):
        return
      result = self.__calculate(self.selected_option2.get(), second, third)
      result = result.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
      result = self.__calculate(self.selected_option1.get(), first, result)
      result = result.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
      result = self.__calculate(self.selected_option3.get(), result, fourth)

      if self.check_result(result):
        messagebox.showerror('Ошибка', 'Результат превышает допустимое значение.')
        return
      
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, self.format_answer(result))
      
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'Ошибка в вычислениях')
  
  def plus(self, first, second):
    try:
      result = first.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP) \
        + second.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP) 
      return result
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'Ошибка при сложении')
      
  def minus(self, first, second):
    try:
      result = first.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP) \
        - second.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
      return result
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'Ошибка при разности')
    
  def mult(self, first, second):
    try:
      result = first.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP) \
        * second.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
      return result
      
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'Ошибка при умножении')
  
  def divide(self, first, second):
    try:
      result = first.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP) \
        / second.quantize(Decimal('0.0000000001'), rounding=ROUND_HALF_UP)
      return result
    
    except ZeroDivisionError as e:
      messagebox.showerror('Ошибка', 'Деление на ноль запрещено!')
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'Деление на ноль запрещено!')
    except:
      self.result.delete(1.0, 'end')
      self.result.insert(1.0, 'Ошибка при делении')
  
  def format_answer(self, number) -> str:
    formatted_result = "{:,.6f}".format(number)
    return formatted_result.replace(',', ' ').rstrip('0').rstrip('.')
  
  def is_valid_number(self, number) -> bool:
    if 'e' in number:
      messagebox.showerror('Ошибка', 'Вы не можете использовать числа в экспоненциальной нотации.')
      return False
    
    try:
      _ = float(number.replace(' ', ''))
    
      pattern = r'^\d{1,3}( \d{3})*(\.\d+)?$'
      if (not number.replace('.', '', 1).rstrip().isdigit()) and (re.match(pattern, number) is None):
        messagebox.showerror('Ошибка', 'Неправильный формат числа.')
        return False
      
        
      if self.check_result(Decimal(number.replace(' ', ''))):
        messagebox.showerror('Ошибка', 'Число превышает допустимое значение.')
        return False
      
      return True
      
    except:
      messagebox.showerror('Ошибка', 'Число введено некорректно.')
    

  
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
  
    