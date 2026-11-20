import tkinter as tk
from tkinter import ttk


class NavigationBar(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        on_restore_code,
        on_first,
        on_previous,
        on_next,
        on_last,
        on_menu,
    ) -> None:
        super().__init__(master, style="App.TFrame")
        left_group = ttk.Frame(self, style="App.TFrame")
        left_group.pack(side="left")
        right_group = ttk.Frame(self, style="App.TFrame")
        right_group.pack(side="right")

        ttk.Button(left_group, text="Restaurar bloque", command=on_restore_code).pack(side="left")

        ttk.Button(right_group, text="Menú principal", command=on_menu).pack(side="left")
        ttk.Button(right_group, text="|<", command=on_first, style="Small.TButton").pack(
            side="left", padx=(8, 0)
        )
        ttk.Button(right_group, text="<", command=on_previous, style="Small.TButton").pack(
            side="left", padx=(6, 0)
        )
        ttk.Button(right_group, text=">", command=on_next, style="Small.TButton").pack(
            side="left", padx=(6, 0)
        )
        ttk.Button(right_group, text=">|", command=on_last, style="Small.TButton").pack(
            side="left", padx=(6, 0)
        )
