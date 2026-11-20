import tkinter as tk
from tkinter import ttk

from app.config import THEME
from app.utils.content_formatter import is_code_like, is_heading_like


class TheoryPanel(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, style="Panel.TFrame")
        self.content: tk.Text | None = None
        self._build()

    def _build(self) -> None:
        body = ttk.Frame(self, style="Panel.TFrame")
        body.pack(fill="both", expand=True)
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.content = tk.Text(
            body,
            wrap="word",
            relief="flat",
            bg=THEME.panel,
            fg=THEME.text,
            font=("Segoe UI", 10),
            padx=6,
            pady=6,
            spacing1=2,
            spacing2=1,
            spacing3=6,
        )
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self.content.yview)
        self.content.configure(yscrollcommand=scrollbar.set)
        self.content.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.content.tag_configure(
            "heading", font=("Segoe UI", 12, "bold"), spacing1=10, spacing3=4
        )
        self.content.tag_configure("paragraph", font=("Segoe UI", 10), lmargin1=6, lmargin2=6)
        self.content.tag_configure("bullet", font=("Segoe UI", 10), lmargin1=18, lmargin2=30)
        self.content.tag_configure(
            "code",
            font=("Consolas", 10),
            background="#eef2f7",
            lmargin1=14,
            lmargin2=14,
            spacing1=4,
            spacing3=4,
        )

    def set_content(self, _title: str, content: str) -> None:
        if self.content is None:
            return
        self.content.configure(state="normal")
        self.content.delete("1.0", "end")
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped:
                self.content.insert("end", "\n")
                continue
            if stripped.startswith(("- ", "* ", "+ ")):
                self.content.insert("end", f"• {stripped[2:]}\n", "bullet")
            elif is_heading_like(stripped):
                self.content.insert("end", f"{stripped}\n", "heading")
            elif is_code_like(stripped):
                self.content.insert("end", f"{stripped}\n", "code")
            else:
                self.content.insert("end", f"{stripped}\n", "paragraph")
        self.content.yview_moveto(0)
        self.content.configure(state="disabled")
