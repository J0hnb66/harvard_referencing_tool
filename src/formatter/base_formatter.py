class BaseFormatter:
    """Base class for all reference formatters with shared Harvard helpers."""

    def format(self, data: dict) -> str:
        raise NotImplementedError("Subclasses must implement this method.")

    # -------------------------
    # Shared Harvard Formatting
    # -------------------------

    def format_authors(self, authors: list[str]) -> str:
        """Format a list of authors into Harvard style."""
        if not authors:
            return ""

        formatted = []
        for name in authors:
            parts = name.split()
            surname = parts[-1]
            initials = "".join([p[0].upper() + "." for p in parts[:-1]])
            formatted.append(f"{surname}, {initials}")

        if len(formatted) == 1:
            return formatted[0]
        elif len(formatted) == 2:
            return f"{formatted[0]} and {formatted[1]}"
        else:
            return ", ".join(formatted[:-1]) + f" and {formatted[-1]}"

    def format_edition(self, edition: str) -> str:
        """Convert edition number into Harvard format."""
        if not edition or edition == "1":
            return ""
        return f"{edition} edn."

    def italic(self, text: str) -> str:
        return text

    def quote(self, text: str) -> str:
        return f"‘{text}’"

    def clean(self, text: str) -> str:
        """Remove double punctuation and tidy spacing."""
        while ".." in text:
            text = text.replace("..", ".")
        return text.strip()
