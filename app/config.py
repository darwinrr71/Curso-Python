from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    bg: str = "#f5f7fb"
    panel: str = "#ffffff"
    panel_alt: str = "#eef2f7"
    border: str = "#d6dde8"
    text: str = "#132238"
    muted: str = "#5b6b82"
    accent: str = "#1769aa"
    accent_soft: str = "#d9ebfb"
    success: str = "#2e7d32"
    danger: str = "#c62828"
    editor_bg: str = "#f8fafc"
    output_bg: str = "#111827"
    output_text: str = "#e5eef9"


THEME = Theme()
