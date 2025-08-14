"""
File Operations

Common file and path operations for Ghostbusters components.
"""

from pathlib import Path
from typing import List


class FileOperations:
    """Safe file and path operations for Ghostbusters components"""

    @staticmethod
    def read_file_safe(file_path: str) -> str:
        """Safely read a file with error handling"""
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            return path.read_text(encoding="utf-8")
        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {e}")

    @staticmethod
    def write_file_safe(file_path: str, content: str) -> bool:
        """Safely write content to a file"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            raise IOError(f"Error writing file {file_path}: {e}")

    @staticmethod
    def ensure_directory(directory_path: str) -> bool:
        """Ensure a directory exists, creating it if necessary"""
        try:
            path = Path(directory_path)
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            raise IOError(f"Error creating directory {directory_path}: {e}")

    @staticmethod
    def list_files(directory_path: str, pattern: str = "*.py") -> List[Path]:
        """List files in a directory matching a pattern"""
        try:
            path = Path(directory_path)
            if not path.exists():
                return []
            return list(path.glob(pattern))
        except Exception:
            return []
