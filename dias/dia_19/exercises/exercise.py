def slugify(text: str) -> str:
    return text.strip().lower().replace(" ", "-")


print(slugify("Python Course"))
