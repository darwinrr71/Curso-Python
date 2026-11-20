import importlib
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk


class LearningApp(tk.Tk):
    def __init__(self, *, dev_mode: bool = False) -> None:
        super().__init__()
        self.dev_mode = dev_mode
        self._current_view = "menu"
        self._current_day: int | None = None
        self._watch_state: dict[Path, int] = {}
        self._reload_pending = False
        self.title("Python 30 Días")
        self.geometry("1500x900")
        self.minsize(1180, 760)
        try:
            self.state("zoomed")
        except tk.TclError:
            pass
        self.container: ttk.Frame | None = None
        self._build_runtime()
        if self.dev_mode:
            self._watch_state = self._snapshot_watched_files()
            self.after(700, self._poll_for_changes)

    def _configure_styles(self, theme) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background=theme.bg)
        style.configure("Panel.TFrame", background=theme.panel)
        style.configure("AltPanel.TFrame", background=theme.panel_alt)
        style.configure(
            "Header.TLabel",
            background=theme.bg,
            foreground=theme.text,
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "SubHeader.TLabel", background=theme.bg, foreground=theme.muted, font=("Segoe UI", 10)
        )
        style.configure(
            "Title.TLabel",
            background=theme.panel,
            foreground=theme.text,
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "Meta.TLabel", background=theme.panel, foreground=theme.muted, font=("Segoe UI", 10)
        )
        style.configure(
            "AltTitle.TLabel",
            background=theme.panel_alt,
            foreground=theme.text,
            font=("Segoe UI", 13, "bold"),
        )
        style.configure(
            "AltMeta.TLabel",
            background=theme.panel_alt,
            foreground=theme.muted,
            font=("Segoe UI", 10),
        )
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Small.TButton", font=("Segoe UI", 9), padding=(6, 2))
        style.configure("SmallPrimary.TButton", font=("Segoe UI", 9, "bold"), padding=(6, 2))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _load_runtime_modules(self, *, reload_modules: bool) -> dict[str, object]:
        module_names = self._runtime_module_names()
        for name in module_names:
            importlib.import_module(name)
        if reload_modules:
            self._reload_runtime_modules(module_names)

        config = importlib.import_module("app.config")
        constants = importlib.import_module("app.constants")
        return {
            "theme": config.THEME,
            "lessons_dir": constants.LESSONS_DIR,
            "progress_file": constants.PROGRESS_FILE,
            "CodeRunner": importlib.import_module("app.services.code_runner").CodeRunner,
            "ContentLoader": importlib.import_module("app.services.content_loader").ContentLoader,
            "LessonRegistry": importlib.import_module("app.services.lesson_registry").LessonRegistry,
            "NavigationService": importlib.import_module("app.services.navigation_service").NavigationService,
            "ProgressService": importlib.import_module("app.services.progress_service").ProgressService,
            "MainMenu": importlib.import_module("app.ui.main_menu").MainMenu,
            "LessonView": importlib.import_module("app.ui.lesson_view").LessonView,
        }

    def _runtime_module_names(self) -> list[str]:
        root = Path(__file__).resolve().parents[2]
        app_dir = root / "app"
        module_names: list[str] = []
        for path in sorted(app_dir.rglob("*.py")):
            if any(part in {".venv", "__pycache__"} for part in path.parts):
                continue
            relative = path.relative_to(root).with_suffix("")
            module_name = ".".join(relative.parts)
            if module_name == "app.ui.app_window":
                continue
            module_names.append(module_name)
        return module_names

    def _reload_runtime_modules(self, module_names: list[str]) -> None:
        for name in module_names:
            module = sys.modules.get(name)
            if module is None:
                module = importlib.import_module(name)
            importlib.reload(module)

    def _build_runtime(self, preserve_state: dict[str, object] | None = None, *, reload_modules: bool = False) -> None:
        runtime = self._load_runtime_modules(reload_modules=reload_modules)
        theme = runtime["theme"]
        self.configure(bg=theme.bg)
        self._configure_styles(theme)

        new_loader = runtime["ContentLoader"](runtime["lessons_dir"])
        new_registry = runtime["LessonRegistry"](runtime["lessons_dir"], new_loader)
        new_lessons = new_registry.all_lessons()
        new_navigation = runtime["NavigationService"](new_lessons)
        new_progress = runtime["ProgressService"](runtime["progress_file"])
        new_runner = runtime["CodeRunner"]()

        new_container = ttk.Frame(self, style="App.TFrame")
        new_main_menu = runtime["MainMenu"](
            master=new_container,
            lessons=new_lessons,
            progress_service=new_progress,
            on_open_lesson=self.open_lesson,
            on_exit=self.destroy,
        )
        new_lesson_view = runtime["LessonView"](
            master=new_container,
            content_loader=new_loader,
            code_runner=new_runner,
            navigation_service=new_navigation,
            on_open_day=self.open_lesson,
            on_back_to_menu=self.show_main_menu,
        )

        old_container = self.container
        new_container.pack(fill="both", expand=True)

        self.loader = new_loader
        self.registry = new_registry
        self.lessons = new_lessons
        self.navigation_service = new_navigation
        self.progress_service = new_progress
        self.code_runner = new_runner
        self.container = new_container
        self.main_menu = new_main_menu
        self.lesson_view = new_lesson_view

        if old_container is not None:
            old_container.destroy()

        if preserve_state and preserve_state.get("view") == "lesson" and preserve_state.get("day"):
            self.open_lesson(
                int(preserve_state["day"]),
                mark_progress=False,
                restore_state=preserve_state.get("lesson_state"),
            )
        else:
            self.show_main_menu(selected_day=preserve_state.get("menu_day") if preserve_state else None)

    def show_main_menu(self, selected_day: int | None = None) -> None:
        self._current_view = "menu"
        self._current_day = None
        self.lesson_view.pack_forget()
        self.main_menu.refresh()
        self.main_menu.pack(fill="both", expand=True)
        if selected_day is not None:
            item_id = str(selected_day)
            if self.main_menu.tree.exists(item_id):
                self.main_menu.tree.selection_set(item_id)
                self.main_menu.tree.focus(item_id)

    def open_lesson(self, day: int, *, mark_progress: bool = True, restore_state: dict[str, object] | None = None) -> None:
        lesson = self.registry.get_by_day(day)
        if mark_progress:
            self.progress_service.mark_visited(day)
        self._current_view = "lesson"
        self._current_day = day
        self.main_menu.pack_forget()
        self.lesson_view.pack(fill="both", expand=True)
        self.lesson_view.render_lesson(lesson)
        if restore_state:
            self.lesson_view.restore_state(restore_state)

    def _iter_watched_paths(self) -> list[Path]:
        root = Path(__file__).resolve().parents[2]
        watch_dirs = ("app", "dias")
        watch_files = ("main.py",)
        watch_suffixes = {".py", ".json", ".md", ".txt"}
        ignore_dirs = {".git", ".venv", ".ruff_cache", "__pycache__", ".pytest_cache"}
        paths: list[Path] = []
        for file_name in watch_files:
            file_path = root / file_name
            if file_path.exists():
                paths.append(file_path)
        for dir_name in watch_dirs:
            base_dir = root / dir_name
            if not base_dir.exists():
                continue
            for path in base_dir.rglob("*"):
                if any(part in ignore_dirs for part in path.parts):
                    continue
                if path.is_file() and path.suffix.lower() in watch_suffixes:
                    paths.append(path)
        return paths

    def _snapshot_watched_files(self) -> dict[Path, int]:
        snapshot: dict[Path, int] = {}
        for path in self._iter_watched_paths():
            try:
                snapshot[path] = path.stat().st_mtime_ns
            except FileNotFoundError:
                continue
        return snapshot

    def _capture_runtime_state(self) -> dict[str, object]:
        state: dict[str, object] = {"view": self._current_view}
        if self._current_view == "lesson" and self._current_day is not None:
            state["day"] = self._current_day
            state["lesson_state"] = self.lesson_view.capture_state()
        else:
            selection = self.main_menu.tree.selection()
            if selection:
                state["menu_day"] = int(selection[0])
        return state

    def _poll_for_changes(self) -> None:
        current_state = self._snapshot_watched_files()
        if current_state != self._watch_state and not self._reload_pending:
            self._watch_state = current_state
            self._reload_pending = True
            self.after(250, self._reload_runtime)
        else:
            self._watch_state = current_state
        self.after(700, self._poll_for_changes)

    def _reload_runtime(self) -> None:
        self._reload_pending = False
        preserved = self._capture_runtime_state()
        try:
            self._build_runtime(preserve_state=preserved, reload_modules=True)
        except Exception as error:
            print(f"Live reload failed: {error}", file=sys.stderr)
