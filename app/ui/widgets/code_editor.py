import tkinter as tk
from tkinter import ttk

from app.config import THEME


class CodeEditor(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, style="Panel.TFrame")
        self.title_label = ttk.Label(self, style="Title.TLabel")
        self.description_label = ttk.Label(self, style="Meta.TLabel", wraplength=450)
        self.expected_label = ttk.Label(self, style="Meta.TLabel", wraplength=450)
        self.editor: tk.Text | None = None
        self.editor_frame: ttk.Frame | None = None
        self._build()

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.title_label.grid(row=0, column=0, sticky="w")
        self.description_label.grid(row=1, column=0, sticky="w", pady=(2, 0))
        self.expected_label.grid(row=2, column=0, sticky="w", pady=(2, 6))
        self.editor_frame = ttk.Frame(self, style="Panel.TFrame")
        self.editor_frame.grid(row=3, column=0, sticky="nsew")
        self.editor_frame.grid_rowconfigure(0, weight=1)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor = tk.Text(
            self.editor_frame,
            wrap="word",
            relief="flat",
            bg=THEME.editor_bg,
            fg=THEME.text,
            insertbackground=THEME.text,
            font=("Consolas", 10),
            height=5,
            undo=True,
        )
        y_scrollbar = ttk.Scrollbar(self.editor_frame, orient="vertical", command=self.editor.yview)
        self.editor.configure(yscrollcommand=y_scrollbar.set)
        self.editor.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")

    def set_title(self, title: str, description: str, expected_output: str) -> None:
        self.title_label.configure(text=title)
        self.description_label.configure(text=description)
        self.expected_label.configure(
            text=f"Resultado esperado: {expected_output}" if expected_output else ""
        )

    def set_code(self, code: str) -> None:
        if self.editor is None:
            return
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", code)
        self.editor.yview_moveto(0)

    def get_code(self) -> str:
        if self.editor is None:
            return ""
        return self.editor.get("1.0", "end").rstrip()
