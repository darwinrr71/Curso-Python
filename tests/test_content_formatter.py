from app.utils.content_formatter import normalize_section_text


def test_normalize_section_text_fixes_common_pdf_artifacts() -> None:
    raw = "\n".join(
        [
            "pythonmain.py",
            "print(TrueandFalse)",
            "1.",
            "pipinstallrequests",
        ]
    )
    normalized = normalize_section_text(raw)
    assert "python main.py" in normalized
    assert "print(True and False)" in normalized
    assert "1." not in normalized
    assert "pip install requests" in normalized
