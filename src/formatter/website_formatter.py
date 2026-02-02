from .base_formatter import BaseFormatter
from utils.helpers import format_author, safe_year, italic
from datetime import datetime


class WebsiteFormatter(BaseFormatter):
    """Formatter for website references."""

    def format(self, data: dict) -> str:
        author = format_author(data.get("author"))
        year = safe_year(data.get("year"))
        title = italic(data.get("title", ""))
        url = data.get("url", "")

        accessed = datetime.now().strftime("%d %B %Y")

        return f"{author} ({year}) {title}. Available at: {url} (Accessed: {accessed})."

