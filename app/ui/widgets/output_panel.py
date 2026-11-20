import tkinter as tk
from tkinter import ttk

from app.config import THEME


class OutputPanel(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, style="AltPanel.TFrame")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        ttk.Label(self, text="Salida de ejecución", style="AltTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )
        self.output: tk.Text | None = None
        body = ttk.Frame(self, style="AltPanel.TFrame")
        body.grid(row=1, column=0, sticky="nsew", pady=(0, 54))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.output = tk.Text(
            body,
            wrap="word",
            relief="flat",
            bg=THEME.output_bg,
            fg=THEME.output_text,
            insertbackground=THEME.output_text,
            font=("Consolas", 10),
            height=1,
        )
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar.set)
        self.output.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns", pady=(0, 54))
        self.output.configure(state="disabled")

    def set_text(self, content: str) -> None:
        if self.output is None:
            return
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", content)
        self.output.yview_moveto(0)
        self.output.configure(state="disabled")

    def clear(self) -> None:
        self.set_text("")
