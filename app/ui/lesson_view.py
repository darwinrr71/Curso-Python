import threading
import tkinter as tk
from tkinter import messagebox, ttk

from app.models import CodeBlock, Lesson, LessonSection
from app.services.code_runner import CodeRunner, ExecutionResult
from app.services.content_loader import ContentLoader
from app.services.navigation_service import NavigationService
from app.ui.widgets.code_editor import CodeEditor
from app.ui.widgets.navigation_bar import NavigationBar
from app.ui.widgets.output_panel import OutputPanel
from app.ui.widgets.summary_preview import SummaryPreview
from app.ui.widgets.theory_panel import TheoryPanel


class LessonView(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        content_loader: ContentLoader,
        code_runner: CodeRunner,
        navigation_service: NavigationService,
        on_open_day,
        on_back_to_menu,
    ) -> None:
        super().__init__(master, style="App.TFrame", padding=16)
        self.content_loader = content_loader
        self.code_runner = code_runner
        self.navigation_service = navigation_service
        self.on_open_day = on_open_day
        self.on_back_to_menu = on_back_to_menu
        self.current_lesson: Lesson | None = None
        self.current_block: CodeBlock | None = None
        self.current_code_original = ""
        self.right_panel_mode = tk.StringVar(value="input")
        self.input_buffer = ""
        self.free_code_buffer = ""
        self._build()

    def _build(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ttk.Frame(self, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header.grid_columnconfigure(0, weight=1)
        self.header_title = ttk.Label(header, style="Header.TLabel")
        self.header_subtitle = SummaryPreview(header)
        self.header_title.grid(row=0, column=0, sticky="w")
        self.header_subtitle.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        body = ttk.Frame(self, style="App.TFrame")
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=0, minsize=320)
        body.grid_columnconfigure(1, weight=1)

        sidebar = ttk.Frame(body, style="Panel.TFrame", padding=16)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(2, weight=3)
        sidebar.grid_rowconfigure(6, weight=2)
        sidebar.grid_columnconfigure(0, weight=1)

        ttk.Label(sidebar, text="Secciones del día", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            sidebar,
            text="Consulta teoría, ejemplos, ejercicios y reto del día.",
            style="Meta.TLabel",
            wraplength=290,
            justify="left",
        ).grid(row=1, column=0, sticky="w", pady=(6, 14))

        section_frame = ttk.Frame(sidebar, style="Panel.TFrame")
        section_frame.grid(row=2, column=0, sticky="nsew")
        section_frame.grid_rowconfigure(0, weight=1)
        section_frame.grid_columnconfigure(0, weight=1)
        self.section_list = tk.Listbox(
            section_frame,
            activestyle="none",
            highlightthickness=0,
            relief="flat",
            exportselection=False,
            font=("Segoe UI", 10),
            height=13,
        )
        section_scroll = ttk.Scrollbar(
            section_frame, orient="vertical", command=self.section_list.yview
        )
        self.section_list.configure(yscrollcommand=section_scroll.set)
        self.section_list.grid(row=0, column=0, sticky="nsew")
        section_scroll.grid(row=0, column=1, sticky="ns")
        self.section_list.bind("<<ListboxSelect>>", self._on_section_selected)

        ttk.Separator(sidebar).grid(row=3, column=0, sticky="ew", pady=14)

        ttk.Label(sidebar, text="Bloques ejecutables", style="Title.TLabel").grid(
            row=4, column=0, sticky="w"
        )
        ttk.Label(
            sidebar,
            text="Carga el bloque en el editor y ejecútalo sin salir de la lección.",
            style="Meta.TLabel",
            wraplength=290,
            justify="left",
        ).grid(row=5, column=0, sticky="w", pady=(6, 14))

        block_frame = ttk.Frame(sidebar, style="Panel.TFrame")
        block_frame.grid(row=6, column=0, sticky="nsew")
        block_frame.grid_rowconfigure(0, weight=1)
        block_frame.grid_columnconfigure(0, weight=1)
        self.code_list = tk.Listbox(
            block_frame,
            activestyle="none",
            highlightthickness=0,
            relief="flat",
            exportselection=False,
            font=("Consolas", 10),
            height=7,
        )
        self.code_list.configure(yscrollcommand=None)
        self.code_list.grid(row=0, column=0, sticky="nsew")
        self.code_list.bind("<<ListboxSelect>>", self._on_code_block_selected)

        workspace = ttk.Frame(body, style="App.TFrame")
        workspace.grid(row=0, column=1, sticky="nsew", padx=(16, 0))
        workspace.grid_rowconfigure(0, weight=5, minsize=300)
        workspace.grid_rowconfigure(1, weight=5, minsize=320)
        workspace.grid_columnconfigure(0, weight=5)
        workspace.grid_columnconfigure(1, weight=3, minsize=420)

        theory_card = ttk.Frame(workspace, style="Panel.TFrame", padding=14)
        theory_card.grid(row=0, column=0, sticky="nsew")
        theory_card.grid_rowconfigure(2, weight=1)
        theory_card.grid_columnconfigure(0, weight=1)
        self.content_title = ttk.Label(theory_card, style="Title.TLabel")
        self.content_meta = ttk.Label(
            theory_card, style="Meta.TLabel", wraplength=980, justify="left"
        )
        self.content_title.grid(row=0, column=0, sticky="w")
        self.content_meta.grid(row=1, column=0, sticky="w", pady=(6, 10))

        theory_host = ttk.Frame(theory_card, style="Panel.TFrame")
        theory_host.grid(row=2, column=0, sticky="nsew")
        theory_host.grid_rowconfigure(0, weight=1)
        theory_host.grid_columnconfigure(0, weight=1)
        self.theory_panel = TheoryPanel(theory_host)
        self.theory_panel.grid(row=0, column=0, sticky="nsew")

        editor_card = ttk.Frame(workspace, style="Panel.TFrame", padding=14)
        editor_card.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        editor_card.grid_rowconfigure(0, weight=1)
        editor_card.grid_columnconfigure(0, weight=1)

        editor_scroll_host = ttk.Frame(editor_card, style="Panel.TFrame")
        editor_scroll_host.grid(row=0, column=0, sticky="nsew")
        editor_scroll_host.grid_rowconfigure(0, weight=1)
        editor_scroll_host.grid_columnconfigure(0, weight=1)

        self.editor_canvas = tk.Canvas(
            editor_scroll_host,
            highlightthickness=0,
            relief="flat",
            background="#ffffff",
        )
        self.editor_canvas.grid(row=0, column=0, sticky="nsew")

        editor_host = ttk.Frame(self.editor_canvas, style="Panel.TFrame")
        self.editor_canvas_window = self.editor_canvas.create_window(
            (0, 0), window=editor_host, anchor="nw"
        )
        editor_host.bind(
            "<Configure>",
            lambda _event: self._refresh_editor_canvas(),
        )
        self.editor_canvas.bind(
            "<Configure>",
            lambda event: self._resize_editor_canvas(event.width),
        )

        self.code_editor = CodeEditor(editor_host)
        self.code_editor.pack(fill="both", expand=True)

        practice_sidebar = ttk.Frame(workspace, style="AltPanel.TFrame", padding=14)
        practice_sidebar.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(14, 0))
        practice_sidebar.grid_rowconfigure(1, weight=1, minsize=150)
        practice_sidebar.grid_rowconfigure(2, weight=1, minsize=280)
        practice_sidebar.grid_columnconfigure(0, weight=1)

        input_panel = ttk.Frame(practice_sidebar, style="AltPanel.TFrame")
        input_panel.grid(row=0, column=0, sticky="ew")
        input_panel.grid_columnconfigure(0, weight=1)
        input_panel.grid_columnconfigure(1, weight=0)
        self.right_panel_title = ttk.Label(
            input_panel, text="Entrada para input()", style="AltTitle.TLabel"
        )
        self.right_panel_title.grid(row=0, column=0, sticky="w")
        quick_actions = ttk.Frame(input_panel, style="AltPanel.TFrame")
        quick_actions.grid(row=0, column=1, rowspan=2, sticky="ne", padx=(10, 0))
        ttk.Button(
            quick_actions,
            text="Limpiar salida",
            command=self._clear_output,
            style="Small.TButton",
        ).pack(side="left")
        self.run_button = ttk.Button(
            quick_actions,
            text="Ejecutar",
            command=self.run_current_code,
            style="SmallPrimary.TButton",
        )
        self.run_button.pack(side="left", padx=(6, 0))
        mode_switch = ttk.Frame(input_panel, style="AltPanel.TFrame")
        mode_switch.grid(row=1, column=0, sticky="w", pady=(6, 0))
        ttk.Radiobutton(
            mode_switch,
            text="Input()",
            value="input",
            variable=self.right_panel_mode,
            command=self._on_right_panel_mode_changed,
        ).pack(side="left")
        ttk.Radiobutton(
            mode_switch,
            text="Código libre",
            value="free_code",
            variable=self.right_panel_mode,
            command=self._on_right_panel_mode_changed,
        ).pack(side="left", padx=(10, 0))
        self.right_panel_meta = ttk.Label(
            input_panel,
            text="Escribe cero o más líneas. Cada llamada a input() usará la siguiente línea en orden.",
            style="AltMeta.TLabel",
            wraplength=380,
            justify="left",
        )
        self.right_panel_meta.grid(row=2, column=0, sticky="w", pady=(6, 8))

        input_editor_frame = ttk.Frame(practice_sidebar, style="AltPanel.TFrame")
        input_editor_frame.grid(row=1, column=0, sticky="nsew", pady=(8, 10))
        input_editor_frame.grid_rowconfigure(0, weight=1)
        input_editor_frame.grid_columnconfigure(0, weight=1)
        self.input_text = tk.Text(
            input_editor_frame,
            height=4,
            wrap="word",
            relief="flat",
            font=("Consolas", 10),
        )
        input_scroll = ttk.Scrollbar(
            input_editor_frame, orient="vertical", command=self.input_text.yview
        )
        self.input_text.configure(yscrollcommand=input_scroll.set)
        self.input_text.grid(row=0, column=0, sticky="nsew")
        input_scroll.grid(row=0, column=1, sticky="ns")

        output_panel_host = ttk.Frame(practice_sidebar, style="AltPanel.TFrame")
        output_panel_host.grid(row=2, column=0, sticky="nsew", pady=(0, 6))
        output_panel_host.grid_rowconfigure(0, weight=1)
        output_panel_host.grid_columnconfigure(0, weight=1)
        self.output_panel = OutputPanel(output_panel_host)
        self.output_panel.grid(row=0, column=0, sticky="nsew")

        self.navigation_bar = NavigationBar(
            self,
            on_restore_code=self.restore_code,
            on_first=self._go_first_day,
            on_previous=self._go_previous_day,
            on_next=self._go_next_day,
            on_last=self._go_last_day,
            on_menu=self.on_back_to_menu,
        )
        self.navigation_bar.grid(row=2, column=0, sticky="ew", pady=(12, 0))

    def render_lesson(self, lesson: Lesson) -> None:
        self.current_lesson = lesson
        self.current_block = None
        self.current_code_original = ""
        self.header_title.configure(text=f"Día {lesson.day:02d} · {lesson.title}")
        self.header_subtitle.set_text(lesson.summary)

        self.section_list.delete(0, "end")
        for section in lesson.sections:
            self.section_list.insert("end", section.title)

        self.code_list.delete(0, "end")
        for block in lesson.code_blocks:
            self.code_list.insert("end", f"[{block.category}] {block.title}")

        self.output_panel.set_text("")
        self.input_buffer = ""
        if self.right_panel_mode.get() == "input":
            self._set_right_panel_text("")

        if lesson.sections:
            self.section_list.selection_clear(0, "end")
            self.section_list.selection_set(0)
            self.section_list.activate(0)
            self.section_list.see(0)
            self._load_section(lesson.sections[0])

        if lesson.code_blocks:
            self.code_list.selection_clear(0, "end")
            self.code_list.selection_set(0)
            self.code_list.activate(0)
            self.code_list.see(0)
            self._load_code_block(lesson.code_blocks[0])
        else:
            self.code_editor.set_title("Sin bloques ejecutables", "", "")
            self.code_editor.set_code("")

    def _on_section_selected(self, _event=None) -> None:
        if not self.current_lesson:
            return
        selection = self.section_list.curselection()
        if selection:
            self._load_section(self.current_lesson.sections[selection[0]])

    def _on_code_block_selected(self, _event=None) -> None:
        if not self.current_lesson:
            return
        selection = self.code_list.curselection()
        if selection:
            self._load_code_block(self.current_lesson.code_blocks[selection[0]])

    def _load_section(self, section: LessonSection) -> None:
        if not self.current_lesson:
            return
        content = self.content_loader.read_section(self.current_lesson, section)
        self.content_title.configure(text=section.title)
        self.content_meta.configure(
            text=f"Contenido del manual para el día {self.current_lesson.day:02d}."
        )
        self.theory_panel.set_content(section.title, content)

    def _load_code_block(self, block: CodeBlock) -> None:
        if not self.current_lesson:
            return
        code = self.content_loader.read_code_block(self.current_lesson, block)
        self.current_block = block
        self.current_code_original = code
        self.code_editor.set_title(block.title, block.description, block.expected_output)
        self.code_editor.set_code(code)
        self.input_buffer = block.default_input
        if self.right_panel_mode.get() == "input":
            self._set_right_panel_text(self.input_buffer)

    def capture_state(self) -> dict[str, object]:
        self._sync_right_panel_buffer()
        section_selection = self.section_list.curselection()
        block_selection = self.code_list.curselection()
        return {
            "day": self.current_lesson.day if self.current_lesson else None,
            "section_index": section_selection[0] if section_selection else 0,
            "block_index": block_selection[0] if block_selection else 0,
            "right_panel_mode": self.right_panel_mode.get(),
            "input_buffer": self.input_buffer,
            "free_code_buffer": self.free_code_buffer,
        }

    def restore_state(self, state: dict[str, object]) -> None:
        if not self.current_lesson:
            return
        section_index = int(state.get("section_index", 0))
        block_index = int(state.get("block_index", 0))

        if self.current_lesson.sections:
            section_index = max(0, min(section_index, len(self.current_lesson.sections) - 1))
            self.section_list.selection_clear(0, "end")
            self.section_list.selection_set(section_index)
            self.section_list.activate(section_index)
            self.section_list.see(section_index)
            self._load_section(self.current_lesson.sections[section_index])

        if self.current_lesson.code_blocks:
            block_index = max(0, min(block_index, len(self.current_lesson.code_blocks) - 1))
            self.code_list.selection_clear(0, "end")
            self.code_list.selection_set(block_index)
            self.code_list.activate(block_index)
            self.code_list.see(block_index)
            self._load_code_block(self.current_lesson.code_blocks[block_index])

        self.input_buffer = str(state.get("input_buffer", ""))
        self.free_code_buffer = str(state.get("free_code_buffer", ""))
        self.right_panel_mode.set(str(state.get("right_panel_mode", "input")))
        self._apply_right_panel_mode()

    def restore_code(self) -> None:
        if self.current_code_original:
            self.code_editor.set_code(self.current_code_original)

    def _get_right_panel_text(self) -> str:
        return self.input_text.get("1.0", "end").rstrip()

    def _set_right_panel_text(self, content: str) -> None:
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", content)
        self.input_text.yview_moveto(0)

    def _on_right_panel_mode_changed(self) -> None:
        self._sync_right_panel_buffer()
        self._apply_right_panel_mode()

    def _sync_right_panel_buffer(self) -> None:
        current_content = self._get_right_panel_text()
        if self.right_panel_mode.get() == "input":
            self.input_buffer = current_content
        else:
            self.free_code_buffer = current_content

    def _apply_right_panel_mode(self) -> None:
        if self.right_panel_mode.get() == "input":
            self.right_panel_title.configure(text="Entrada para input()")
            self.right_panel_meta.configure(
                text="Escribe cero o más líneas. Cada llamada a input() usará la siguiente línea en orden."
            )
            self._set_right_panel_text(self.input_buffer)
        else:
            self.right_panel_title.configure(text="Código libre")
            self.right_panel_meta.configure(
                text="Pega o escribe un snippet Python y ejecútalo desde aquí sin cambiar el bloque de la lección."
            )
            self._set_right_panel_text(self.free_code_buffer)

    def _refresh_editor_canvas(self) -> None:
        self.editor_canvas.configure(scrollregion=self.editor_canvas.bbox("all"))

    def _resize_editor_canvas(self, width: int) -> None:
        self.editor_canvas.itemconfigure(self.editor_canvas_window, width=width)
        self._refresh_editor_canvas()

    def run_current_code(self) -> None:
        if self.right_panel_mode.get() == "free_code":
            code = self._get_right_panel_text()
            self.free_code_buffer = code
            stdin_text = ""
            empty_message = "Escribe un bloque de código libre antes de ejecutarlo."
        else:
            code = self.code_editor.get_code()
            stdin_text = self.input_text.get("1.0", "end").strip("\n")
            self.input_buffer = stdin_text
            empty_message = "Selecciona o escribe un bloque de código antes de ejecutarlo."
        if not code.strip():
            messagebox.showinfo("Código vacío", empty_message)
            return

        self._set_running_state(True)
        self.output_panel.set_text("Ejecutando...\n")

        def worker() -> None:
            result = self.code_runner.execute(code, stdin_text)
            self.after(0, lambda: self._show_execution_result(result))

        threading.Thread(target=worker, daemon=True).start()

    def _clear_output(self) -> None:
        self.output_panel.clear()

    def _show_execution_result(self, result: ExecutionResult) -> None:
        parts = []
        if result.stdout:
            parts.append("STDOUT\n" + result.stdout)
        if result.stderr:
            parts.append("STDERR\n" + result.stderr)
        if not parts:
            parts.append("La ejecución terminó sin salida.")
        self.output_panel.set_text("\n\n".join(parts))
        self._set_running_state(False)

    def _set_running_state(self, running: bool) -> None:
        self.run_button.state(["disabled"] if running else ["!disabled"])

    def _go_previous_day(self) -> None:
        if not self.current_lesson:
            return
        previous_day = self.navigation_service.previous_day(self.current_lesson.day)
        if previous_day is not None:
            self.on_open_day(previous_day)

    def _go_next_day(self) -> None:
        if not self.current_lesson:
            return
        next_day = self.navigation_service.next_day(self.current_lesson.day)
        if next_day is not None:
            self.on_open_day(next_day)

    def _go_first_day(self) -> None:
        first_day = self.navigation_service.first_day()
        if first_day is not None:
            self.on_open_day(first_day)

    def _go_last_day(self) -> None:
        last_day = self.navigation_service.last_day()
        if last_day is not None:
            self.on_open_day(last_day)
