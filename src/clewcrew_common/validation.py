"""
Validation Utilities

Common validation patterns for Ghostbusters components.
"""

import re
from typing import Any, Dict, List, Optional


class ValidationUtils:
    """Common validation utilities for Ghostbusters components"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address format"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_required_fields(
        data: Dict[str, Any], required_fields: List[str]
    ) -> List[str]:
        """Validate that required fields are present in data"""
        errors = []
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")
        return errors

    @staticmethod
    def validate_string_length(
        value: str, min_length: int = 0, max_length: Optional[int] = None
    ) -> bool:
        """Validate string length constraints"""
        if not isinstance(value, str):
            return False

        if len(value) < min_length:
            return False

        if max_length is not None and len(value) > max_length:
            return False

        return True

    @staticmethod
    def validate_numeric_range(
        value: Any, min_value: Optional[float] = None, max_value: Optional[float] = None
    ) -> bool:
        """Validate numeric value is within range"""
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            return False

        if min_value is not None and num_value < min_value:
            return False

        if max_value is not None and num_value > max_value:
            return False

        return True
