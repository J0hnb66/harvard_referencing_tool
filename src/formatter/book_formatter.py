from .base_formatter import BaseFormatter
from utils.helpers import format_author, safe_year, italic


class BookFormatter(BaseFormatter):
    """Formatter for book references using Harvard rules."""

    def format(self, data: dict) -> str:
        author = format_author(data.get("author"))
        year = safe_year(data.get("year"))
        title = italic(data.get("title", ""))
        publisher = data.get("publisher", "")

        return f"{author} ({year}) {title}. {publisher}."

