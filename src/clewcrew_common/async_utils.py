"""
Async Utilities

Common async patterns and utilities for Ghostbusters components.
"""

import asyncio
from typing import Any, Callable, Optional


class AsyncExecutor:
    """Execute async operations with retry logic and timeout handling"""

    def __init__(self, default_timeout: int = 30, default_retries: int = 3):
        """Initialize the async executor"""
        self.default_timeout = default_timeout
        self.default_retries = default_retries

    async def execute_with_retry(
        self,
        operation: Callable,
        max_retries: Optional[int] = None,
        timeout: Optional[int] = None,
        *args,
        **kwargs,
    ) -> Any:
        """Execute an async operation with retry logic"""
        max_retries = max_retries or self.default_retries
        timeout = timeout or self.default_timeout

        for attempt in range(max_retries + 1):
            try:
                return await asyncio.wait_for(
                    operation(*args, **kwargs), timeout=timeout
                )
            except asyncio.TimeoutError:
                if attempt == max_retries:
                    raise
                await asyncio.sleep(1 * (2**attempt))  # Exponential backoff
            except Exception:
                if attempt == max_retries:
                    raise
                await asyncio.sleep(1 * (2**attempt))  # Exponential backoff
