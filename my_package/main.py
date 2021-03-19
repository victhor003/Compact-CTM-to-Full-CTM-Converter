import tkinter as tk
from tkinter import ttk
from my_package import CTMmode as ctm
from my_package import OverlayMode as overlaytab
import os
import sys

class Window(tk.Tk):
    def __init__(self, title, geometry, icon, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.root = tk.Frame(self)
        self.root.grid(row=0, column=0, sticky='nswe')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.title(title)
        self.geometry(geometry)
        self.wm_iconbitmap(icon)
        self.resizable(False, False)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.grid(row=0, column=0, pady=15)

        self.ctmtab = ctm.CTMTab(self.tabs)
        self.ctmtab.grid(row=1, column=0, columnspan=2)

        self.overlaytab = overlaytab.OverlayTab(self.tabs)
        # self.overlaytab.grid(row=1, column=0, columnspan=2)

        self.tabs.add(self.ctmtab, text='CTM', padding=2)
        self.tabs.add(self.overlaytab, text='Overlay', padding=2)



def img_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    icon_path = img_resource_path('appicon.ico')
    main_window = Window('Compact CTM to Full CTM Converter - by victhor003', '970x720',icon_path)
    main_window.mainloop()

if __name__ == '__main__':
    main()
