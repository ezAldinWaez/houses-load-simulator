import tkinter as tk

from houses_load_sim import HousesLoadSimulator


if __name__ == "__main__":
    root = tk.Tk()
    HousesLoadSimulator(root, num_houses=9)
    root.mainloop()
