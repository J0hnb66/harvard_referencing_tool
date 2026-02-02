from .base_formatter import BaseFormatter

class WebsiteFormatter(BaseFormatter):
    """Formatter for website references."""

    def format(self, data: dict) -> str:
        # Placeholder logic
        return f"{data.get('author', '')} ({data.get('year', '')}). {data.get('title', '')}. Retrieved from {data.get('url', '')}"
