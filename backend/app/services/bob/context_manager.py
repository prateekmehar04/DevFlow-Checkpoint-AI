from __future__ import annotations

import json
from typing import Any, Dict, Optional

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from ...config import settings
from ...storage import store


class ContextManager:
    """
    Manages workflow context with Redis caching and PostgreSQL persistence.
    Falls back to JSON storage if Redis is not available.
    """
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.cache_ttl = settings.redis_cache_ttl
        
        # Initialize Redis if available and configured
        if REDIS_AVAILABLE and settings.redis_url and settings.redis_url != "redis://localhost:6379/0":
            try:
                self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            except Exception:
                self.redis_client = None
    
    async def save_context(self, workflow_id: str, context_data: Dict[str, Any]) -> None:
        """
        Save context to Redis cache and persistent storage.
        
        Args:
            workflow_id: Workflow identifier
            context_data: Context data to save
        """
        # Save to Redis cache if available
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"context:{workflow_id}",
                    self.cache_ttl,
                    json.dumps(context_data)
                )
            except Exception:
                pass  # Fail silently, will use persistent storage
        
        # Save to persistent storage (JSON for now, will be PostgreSQL)
        store.save_context(workflow_id, context_data)
    
    async def load_context(self, workflow_id: str) -> Dict[str, Any]:
        """
        Load context from Redis cache or persistent storage.
        
        Args:
            workflow_id: Workflow identifier
            
        Returns:
            Context data dictionary
        """
        # Try Redis cache first
        if self.redis_client:
            try:
                cached = await self.redis_client.get(f"context:{workflow_id}")
                if cached:
                    return json.loads(cached)
            except Exception:
                pass  # Fall through to persistent storage
        
        # Fallback to persistent storage
        return store.load_context(workflow_id)
    
    def merge_contexts(self, base_context: Dict[str, Any], new_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge two context dictionaries.
        
        Args:
            base_context: Base context
            new_context: New context to merge
            
        Returns:
            Merged context dictionary
        """
        merged = dict(base_context)
        for key, value in new_context.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = self.merge_contexts(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def compress_context(self, context: Dict[str, Any], max_tokens: int = 100000) -> Dict[str, Any]:
        """
        Compress context to fit within token limits.
        
        Args:
            context: Context to compress
            max_tokens: Maximum tokens allowed
            
        Returns:
            Compressed context dictionary
        """
        max_chars = max_tokens * 4
        serialized = json.dumps(context, sort_keys=True)
        if len(serialized) <= max_chars:
            return context
        return {
            "summary": serialized[: max_chars - 200],
            "truncated": True,
            "original_keys": sorted(context.keys()),
        }
    
    async def close(self) -> None:
        """Close Redis connection if open."""
        if self.redis_client:
            await self.redis_client.close()
