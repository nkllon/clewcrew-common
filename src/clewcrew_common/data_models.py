"""
Data Models

Common Pydantic models for Ghostbusters components.
"""

from pydantic import BaseModel, Field
from typing import Any, Dict


class BaseResult(BaseModel):
    """Base result model for all Ghostbusters operations"""

    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Human-readable message about the result")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class BaseConfig(BaseModel):
    """Base configuration model for Ghostbusters components"""

    name: str = Field(..., description="Configuration name")
    enabled: bool = Field(
        default=True, description="Whether this configuration is enabled"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional configuration metadata"
    )
