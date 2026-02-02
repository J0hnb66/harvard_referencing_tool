class BaseFormatter:
    """Base class for all reference formatters."""

    def format(self, data: dict) -> str:
        raise NotImplementedError("Subclasses must implement this method.")
