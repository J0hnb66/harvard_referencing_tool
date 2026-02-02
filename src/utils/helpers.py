def format_author(author: str) -> str:
    """Convert 'John Smith' into 'Smith, J.' and handle multiple authors."""
    if not author:
        return ""

    authors = [a.strip() for a in author.split(",")]

    formatted = []
    for person in authors:
        parts = person.split()
        surname = parts[-1]
        initials = "".join([p[0].upper() + "." for p in parts[:-1]])
        formatted.append(f"{surname}, {initials}")

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]} and {formatted[1]}"
    else:
        return f"{formatted[0]} et al."


def safe_year(year: str) -> str:
    return year if year else "n.d."


def italic(text: str) -> str:
    return f"*{text}*"
