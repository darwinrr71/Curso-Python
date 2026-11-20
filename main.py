import os
import tkinter as tk

from app.ui.app_window import LearningApp


def main() -> None:
    try:
        app = LearningApp(dev_mode=os.environ.get("PYTHON_30_DIAS_DEV") == "1")
    except tk.TclError as error:
        error_text = str(error)
        if "init.tcl" in error_text or "Tcl/Tk runtime" in error_text:
            message = (
                "Tkinter could not start because the Python installation does not have a working "
                "Tcl/Tk runtime. Install Python with Tk support and try again.\n\n"
                f"Original error: {error}"
            )
        else:
            message = (
                "The application failed while building the Tkinter interface.\n\n"
                f"Original error: {error}"
            )
        print(message)
        raise SystemExit(1) from error
    app.mainloop()


if __name__ == "__main__":
    main()
