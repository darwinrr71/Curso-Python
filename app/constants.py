from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
LESSONS_DIR = ROOT_DIR / "dias"
DATA_DIR = ROOT_DIR / "data"
PROGRESS_FILE = DATA_DIR / "progress.json"
