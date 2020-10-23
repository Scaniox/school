import tkinter as tk
from tkinter import ttk

s = 0
u = 0
v = 0
a = 0
t = 0

root = tk.Tk()

ui_elements = {}

for var in ["s","u","v","a","t"]:
    label = tk.Label(text=f"{var}:", linked_variable=exec(var))
