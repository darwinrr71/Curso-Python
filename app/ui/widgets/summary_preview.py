import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk


class SummaryPreview(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        *,
        style_name: str = "SubHeader.TLabel",
        tooltip_delay_ms: int = 350,
    ) -> None:
        super().__init__(master, style="App.TFrame")
        self._style_name = style_name
        self._tooltip_delay_ms = tooltip_delay_ms
        self._full_text = ""
        self._first_line = ""
        self._display_text = ""
        self._tooltip_job: str | None = None
        self._tooltip_window: tk.Toplevel | None = None

        self.grid_columnconfigure(0, weight=1)
        self.label = ttk.Label(self, style=style_name, justify="left", anchor="w")
        self.label.grid(row=0, column=0, sticky="ew")

        self.bind("<Configure>", self._schedule_render)
        self.label.bind("<Configure>", self._schedule_render)
        self.label.bind("<Enter>", self._schedule_tooltip)
        self.label.bind("<Leave>", self._hide_tooltip)
        self.label.bind("<ButtonPress>", self._hide_tooltip)

    def set_text(self, text: str) -> None:
        self._full_text = text.strip()
        lines = [line.strip() for line in self._full_text.splitlines() if line.strip()]
        self._first_line = lines[0] if lines else self._full_text
        self._schedule_render()

    def _schedule_render(self, _event=None) -> None:
        self.after_idle(self._render)

    def _render(self) -> None:
        if not self.winfo_exists():
            return
        width = self.winfo_width() or self.label.winfo_width()
        if width <= 10:
            return

        font = self._resolve_font()
        available_width = max(width - 12, 40)
        first_line = self._first_line
        if not first_line:
            self._display_text = ""
            self.label.configure(text="")
            return

        if font.measure(first_line) <= available_width:
            self._display_text = first_line
            self.label.configure(text=first_line)
            return

        ellipsis = "..."
        low, high = 0, len(first_line)
        best = ellipsis
        while low <= high:
            middle = (low + high) // 2
            candidate = first_line[:middle].rstrip() + ellipsis
            if font.measure(candidate) <= available_width:
                best = candidate
                low = middle + 1
            else:
                high = middle - 1
        self._display_text = best
        self.label.configure(text=best)

    def _resolve_font(self) -> tkfont.Font:
        style = ttk.Style(self)
        font_spec = style.lookup(self._style_name, "font") or self.label.cget("font") or "TkDefaultFont"
        return tkfont.Font(font=font_spec)

    def _should_show_tooltip(self) -> bool:
        return bool(self._full_text) and self._display_text != self._full_text

    def _schedule_tooltip(self, _event=None) -> None:
        if not self._should_show_tooltip():
            return
        self._cancel_tooltip_job()
        self._tooltip_job = self.after(self._tooltip_delay_ms, self._show_tooltip)

    def _cancel_tooltip_job(self) -> None:
        if self._tooltip_job is not None:
            self.after_cancel(self._tooltip_job)
            self._tooltip_job = None

    def _show_tooltip(self) -> None:
        self._tooltip_job = None
        if not self._should_show_tooltip() or self._tooltip_window is not None:
            return

        tooltip = tk.Toplevel(self)
        tooltip.wm_overrideredirect(True)
        tooltip.attributes("-topmost", True)
        tooltip.configure(bg="#ffffff", padx=1, pady=1)

        label = tk.Label(
            tooltip,
            text=self._full_text,
            justify="left",
            anchor="w",
            bg="#ffffff",
            fg="#1e293b",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 10),
            padx=10,
            pady=8,
            wraplength=max(500, self.winfo_toplevel().winfo_width() - 160),
        )
        label.pack()

        x = self.label.winfo_rootx()
        y = self.label.winfo_rooty() + self.label.winfo_height() + 6
        tooltip.geometry(f"+{x}+{y}")
        self._tooltip_window = tooltip

    def _hide_tooltip(self, _event=None) -> None:
        self._cancel_tooltip_job()
        if self._tooltip_window is not None:
            self._tooltip_window.destroy()
            self._tooltip_window = None
