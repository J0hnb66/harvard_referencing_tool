from .base_formatter import BaseFormatter

class BookFormatter(BaseFormatter):
    """Formatter for book references."""

    def format(self, data: dict) -> str:
        # Placeholder logic
        return f"{data.get('author', '')} ({data.get('year', '')}). {data.get('title', '')}."
