import tkinter as tk
from tkinter import ttk

from app.models import Lesson
from app.services.progress_service import ProgressService


class MainMenu(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        lessons: list[Lesson],
        progress_service: ProgressService,
        on_open_lesson,
        on_exit,
    ) -> None:
        super().__init__(master, style="App.TFrame", padding=24)
        self.lessons = lessons
        self.progress_service = progress_service
        self.on_open_lesson = on_open_lesson
        self.on_exit = on_exit
        self.tree = ttk.Treeview(
            self,
            columns=("day", "title", "status"),
            show="headings",
            selectmode="browse",
        )
        self.progress_label = ttk.Label(self, style="SubHeader.TLabel")
        self._build()

    def _build(self) -> None:
        header = ttk.Frame(self, style="App.TFrame")
        header.pack(fill="x", pady=(0, 18))
        ttk.Label(header, text="Manual de Python en 30 días", style="Header.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            header,
            text="Aplicación educativa de escritorio con teoría, ejemplos ejecutables, ejercicios y mini retos.",
            style="SubHeader.TLabel",
        ).pack(anchor="w", pady=(6, 0))
        self.progress_label.pack(anchor="w", pady=(8, 0))

        card = ttk.Frame(self, style="Panel.TFrame", padding=18)
        card.pack(fill="both", expand=True)

        self.tree.heading("day", text="Día")
        self.tree.heading("title", text="Lección")
        self.tree.heading("status", text="Estado")
        self.tree.column("day", width=90, anchor="center")
        self.tree.column("title", width=800, anchor="w")
        self.tree.column("status", width=140, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self._open_selected)

        footer = ttk.Frame(self, style="App.TFrame")
        footer.pack(fill="x", pady=(16, 0))
        ttk.Button(
            footer, text="Abrir día", command=self._open_selected, style="Primary.TButton"
        ).pack(side="left")
        ttk.Button(footer, text="Cerrar aplicación", command=self.on_exit).pack(side="right")

    def refresh(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for lesson in self.lessons:
            status = "Visto" if self.progress_service.is_visited(lesson.day) else "Pendiente"
            self.tree.insert(
                "", "end", iid=str(lesson.day), values=(f"{lesson.day:02d}", lesson.title, status)
            )
        visited = self.progress_service.visited_count()
        self.progress_label.configure(text=f"Progreso local: {visited}/30 días visitados")
        if self.lessons:
            self.tree.selection_set(str(self.lessons[0].day))

    def _open_selected(self, _event=None) -> None:
        selection = self.tree.selection()
        if not selection:
            return
        self.on_open_lesson(int(selection[0]))
