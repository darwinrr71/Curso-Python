from __future__ import annotations

import os

from main import main


def run() -> int:
    os.environ["PYTHON_30_DIAS_DEV"] = "1"
    main()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
