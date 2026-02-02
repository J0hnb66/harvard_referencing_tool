class InputValidator:
    """Validates required fields for reference generation."""

    @staticmethod
    def validate_required_fields(data: dict, required: list):
        missing = [field for field in required if field not in data or not data[field]]
        return missing
