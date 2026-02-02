from .base_formatter import BaseFormatter

class JournalFormatter(BaseFormatter):
    """Formatter for journal article references."""

    def format(self, data: dict) -> str:
        # Placeholder logic
        return f"{data.get('author', '')} ({data.get('year', '')}). {data.get('title', '')}."
