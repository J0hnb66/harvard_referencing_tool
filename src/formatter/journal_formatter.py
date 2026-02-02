from .base_formatter import BaseFormatter
from utils.helpers import format_author, safe_year, italic


class JournalFormatter(BaseFormatter):
    """Formatter for journal article references."""

    def format(self, data: dict) -> str:
        author = format_author(data.get("author"))
        year = safe_year(data.get("year"))
        title = f"‘{data.get('title', '')}’"
        journal = italic(data.get("journal", ""))
        volume = data.get("volume", "")
        issue = data.get("issue", "")
        pages = data.get("pages", "")

        return f"{author} ({year}) {title}, {journal}, {volume}({issue}), {pages}."
