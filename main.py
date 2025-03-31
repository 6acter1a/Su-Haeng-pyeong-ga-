import sys
import os
import tkinter as tk
from tkinter import messagebox
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reaction_calculator import ChemicalReaction

def calculate():
    equation = entry_equation.get()
    reaction = ChemicalReaction(equation)
    
    given_masses = {}
    for reactant in reaction.reactants:
        try:
            mass = float(entries[reactant].get())
            given_masses[reactant] = mass
        except ValueError:
            messagebox.showerror("Input Error", f"Invalid mass for {reactant}")
            return
    
    molar_masses = {}
    for compound in set(reaction.reactants.keys()).union(set(reaction.products.keys())):
        molar_mass = reaction.calculate_molar_mass(compound)
        molar_masses[compound] = molar_mass
    
    result = reaction.calculate_mass(given_masses, molar_masses)
    
    output_text.set("Remaining Reactants:\n")
    for reactant, mass in result['reactants_left'].items():
        output_text.set(output_text.get() + f"{reactant}: {mass:.2f} g\n")
    
    output_text.set(output_text.get() + "\nProducts Formed:\n")
    for product, mass in result['products'].items():
        output_text.set(output_text.get() + f"{product}: {mass:.2f} g\n")

def setup_ui():
    global entry_equation, entries, output_text
    
    root = tk.Tk()
    root.title("Chemical Reaction Calculator")
    
    tk.Label(root, text="Enter chemical equation:").pack()
    entry_equation = tk.Entry(root, width=50)
    entry_equation.pack()
    
    tk.Button(root, text="Submit Equation", command=setup_mass_inputs).pack()
    
    root.mainloop()

def setup_mass_inputs():
    equation = entry_equation.get()
    reaction = ChemicalReaction(equation)
    
    global entries, output_text
    entries = {}
    mass_window = tk.Toplevel()
    mass_window.title("Enter Masses")
    
    for reactant in reaction.reactants:
        tk.Label(mass_window, text=f"Mass of {reactant} (g):").pack()
        entry = tk.Entry(mass_window)
        entry.pack()
        entries[reactant] = entry
    
    tk.Button(mass_window, text="Calculate", command=calculate).pack()
    
    output_text = tk.StringVar()
    output_label = tk.Label(mass_window, textvariable=output_text, justify="left")
    output_label.pack()

def main():
    setup_ui()

if __name__ == "__main__":
    main()
