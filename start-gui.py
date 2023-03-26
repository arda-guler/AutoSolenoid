import tkinter as tk
from tkinter import ttk
import sys

from autosolenoid import autoAnalyze

head_offset = 5
N_entries = 0
abs_column = 0

entries = []
text_entries = []
entry_unit_vars = []

class entry:
    def __init__(self, entry_field, entry_label, unit, unit_type):
        self.entry_field = entry_field
        self.entry_label = entry_label
        self.unit = unit
        self.unit_type = unit_type

    def get_value(self):
        if not self.entry_field.get("1.0", "end-1c") == "":
            if self.unit_type == "float":
                return float(self.entry_field.get("1.0", "end-1c"))
            elif self.unit_type == "int":
                return int(float(self.entry_field.get("1.0", "end-1c")))
            elif self.unit_type == "string":
                return self.entry_field.get("1.0", "end-1c")
        else:
            return 0

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return("break")

def show_about():
    about_win = tk.Toplevel()
    about_win.title("About AutoSolenoid")
    about_text = "Automatically generate finite element models and perform full-stroke analysis on solenoid actuator designs.\n"
    about_text += "Written by H. A. Güler (arda-guler @ Github). Licensed under MIT License.\n\n"
    about_text += "Find the source code here: https://github.com/arda-guler/AutoSolenoid"
    about_label = tk.Label(about_win, text=about_text)
    about_label.pack()

def create_entry(label, units, unit_type):
    global N_entries, entries, head_offset, text_entries, entry_unit_vars

    abs_offset = head_offset + N_entries

    entry_unit = tk.StringVar()
    entry_unit.set(units)
    entry_unit_vars.append(entry_unit)
    
    new_label = tk.Label(mw, text=label, anchor='e')
    new_label.grid(row = abs_offset, column = 0 + abs_column*3, sticky="e")
    
    new_textfield = tk.Text(mw, height=1, width=10)
    new_textfield.grid(row = abs_offset, column = 1 + abs_column*3)
    new_textfield.bind("<Tab>", focus_next_widget)
    text_entries.append(new_textfield)

    new_unitdisplay = tk.Label(mw, text=units, anchor='w')
    new_unitdisplay.config(width=20)
    new_unitdisplay.grid(row = abs_offset, column=2 + abs_column*3)

    new_entry = entry(new_textfield, label, entry_unit, unit_type)
    entries.append(new_entry)

    N_entries += 1

def create_label(label):
    global N_entries, head_offset

    abs_offset = head_offset + N_entries

    new_label = tk.Label(mw, text=label)
    new_label.grid(row = abs_offset, column = 0 + abs_column*3, columnspan=3)

    N_entries += 1

def start_analysis():
    params = []
    for entry in entries:
        cvalue = entry.get_value()
        params.append(cvalue)

    autoAnalyze(params)

print("Please don't close this window while working with AutoSolenoid.")

mw = tk.Tk()
mw.title("AutoSolenoid")
mw.iconbitmap('icon.ico')

analyze_button = tk.Button(mw, text="PERFORM ANALYSIS", width=25, height=1, font=("Arial",17), command=start_analysis, bg="red", fg="white")
analyze_button.grid(row=0, column=6, columnspan=3, rowspan=3)

about_button = tk.Button(mw, text="About", command=show_about)
about_button.grid(row=0, column=3, columnspan=3, rowspan=2)

hsep1 = ttk.Separator(mw, orient='horizontal')
hsep1.place(x=0, y=60, relwidth=1, relheight=0.2)

inputs_label = tk.Label(mw, text="DESIGN PARAMETERS", font=("Arial", 13))
inputs_label.grid(row=3, column=0, columnspan=9)

create_label("Solenoid Coil")
create_entry("Number of Turns", "mm", "int")
create_entry("Winding Length", "mm", "float")
create_entry("Current", "A", "float")
create_entry("Winding Radius", "mm", "float")
create_entry("Wire Diameter", "mm", "float")

abs_column += 1
N_entries = 0

create_label("Plunger")
create_entry("Outer Radius", "mm", "float")
create_entry("Axial Length", "mm", "float")
create_entry("Spring Housing Radius", "mm", "float")
create_entry("Spring Housing Depth", "mm", "float")
create_entry("Plunger Material", "<FEMM_Material>", "string")
create_entry("Stroke Length", "mm", "float")

abs_column += 1
N_entries = 0

create_label("Magnetic Core/Casing")
create_entry("Core Inner Radius", "mm", "float")
create_entry("Core Inner Length", "mm", "float")
create_entry("Core Outer Shell Thickness", "mm", "float")
create_entry("Core Closed Side Thickness", "mm", "float")
create_entry("Core Action Side Thickness", "mm", "float")
create_entry("Core Material", "<FEMM_Material>", "string")

create_label("")
create_label("Analysis Settings")
create_entry("Stroke Step", "mm", "float")
create_entry("View Edge Padding", "mm", "float")
create_entry("Export Filename", "<None>", "string")
create_entry("Export Video", "(0/1)", "int")
create_entry("Density Plot Max.", "T", "float")

mw.mainloop()
