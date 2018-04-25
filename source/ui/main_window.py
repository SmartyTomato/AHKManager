from tkinter import ttk

from source.ui.window import create_window
from ..configure import configs

import logging
import tkinter


class MainWindow:

    def __init__(self):
        logging.info("Creating main window")
        main_window = create_window(configs.window.width,
                                    configs.window.height)
        main_window.title("AHK Manager")

        rows = 0
        while rows < 50:
            main_window.rowconfigure(rows, weight=1)
            main_window.columnconfigure(rows, weight=1)
            rows += 1

        notebook = ttk.Notebook(main_window)
        notebook.grid(row=1, column=0, columnspan=50, rowspan=49, sticky='NESW')

        page1 = ttk.Frame(notebook)
        notebook.add(page1, text="tab1")

        page2 = ttk.Frame(notebook)
        notebook.add(page2, text="tab2")

        main_window.mainloop()
