# main.py
import tkinter as tk
from modules.gui import SocialGraphApp

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialGraphApp(root)
    root.mainloop()