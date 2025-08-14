"""
Configuration Management

Environment and configuration management for Ghostbusters components.
"""

import os
from typing import Any, Optional


class ConfigManager:
    """Centralized configuration management for Ghostbusters components"""

    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager"""
        self.config_file = config_file
        self._config_cache = {}

    def get(
        self,
        key: str,
        default: Any = None,
        required: bool = False,
        type_hint: Optional[type] = None,
    ) -> Any:
        """Get configuration value with fallback to default"""
        # Check environment variables first
        value = os.getenv(key, default)

        # Check config file if specified
        if value is None and self.config_file:
            value = self._get_from_file(key, default)

        # Validate required values
        if required and value is None:
            raise ValueError(f"Required configuration '{key}' not found")

        # Type conversion if specified
        if value is not None and type_hint:
            try:
                if type_hint == bool:
                    value = self._parse_bool(value)
                else:
                    value = type_hint(value)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid type for configuration '{key}': {e}")

        return value

    def _get_from_file(self, key: str, default: Any) -> Any:
        """Get configuration from file (placeholder for future implementation)"""
        # TODO: Implement config file parsing
        return default

    def _parse_bool(self, value: Any) -> bool:
        """Parse boolean values from various formats"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes", "on")
        if isinstance(value, (int, float)):
            return bool(value)
        return False

    def set(self, key: str, value: Any):
        """Set configuration value (for testing/debugging)"""
        self._config_cache[key] = value

    def has(self, key: str) -> bool:
        """Check if configuration key exists"""
        return os.getenv(key) is not None or key in self._config_cache


# Global configuration instance
config = ConfigManager()


def get_config() -> ConfigManager:
    """Get global configuration instance"""
    return config
