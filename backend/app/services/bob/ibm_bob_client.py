"""IBM BOB API Client."""

import json
from typing import Any, AsyncGenerator, Dict, Optional

import httpx

from ...config import settings


class IBMBobClient:
    """Client for IBM BOB API."""
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or settings.ibm_bob_api_key
        self.api_url = api_url or settings.ibm_bob_api_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_message(
        self,
        model: str,
        max_tokens: int,
        temperature: float,
        system: str,
        messages: list,
    ) -> Dict[str, Any]:
        """
        Create a message using IBM BOB API.
        
        Args:
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            system: System prompt
            messages: List of message dictionaries
            
        Returns:
            Response dictionary with generated content
        """
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system,
            "messages": messages
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_url}/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {
                    "error": str(e),
                    "content": [{"text": f"Error calling IBM BOB API: {str(e)}"}]
                }
    
    async def stream_message(
        self,
        model: str,
        max_tokens: int,
        temperature: float,
        system: str,
        messages: list,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a message using IBM BOB API.
        
        Args:
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            system: System prompt
            messages: List of message dictionaries
            
        Yields:
            Text chunks from the stream
        """
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system,
            "messages": messages,
            "stream": True
        }
        
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream(
                    "POST",
                    f"{self.api_url}/messages/stream",
                    headers=self.headers,
                    json=payload,
                    timeout=60.0
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]  # Remove "data: " prefix
                            if data.strip() and data != "[DONE]":
                                try:
                                    chunk = json.loads(data)
                                    if "text" in chunk:
                                        yield chunk["text"]
                                except json.JSONDecodeError:
                                    continue
            except httpx.HTTPError as e:
                yield f"Error streaming from IBM BOB API: {str(e)}"


class AsyncBobMessages:
    """Async context manager for streaming messages."""
    
    def __init__(self, client: IBMBobClient, **kwargs):
        self.client = client
        self.kwargs = kwargs
        self._generator = None
    
    async def __aenter__(self):
        self._generator = self.client.stream_message(**self.kwargs)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._generator:
            await self._generator.aclose()
    
    @property
    def text_stream(self):
        """Get the text stream generator."""
        return self._generator


class AsyncIBMBobClient:
    """Async IBM BOB client with Anthropic-compatible interface."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = IBMBobClient(api_key=api_key)
        self.messages = self
    
    async def create(self, **kwargs) -> Dict[str, Any]:
        """Create a message (Anthropic-compatible interface)."""
        return await self.client.create_message(**kwargs)
    
    def stream(self, **kwargs) -> AsyncBobMessages:
        """Stream a message (Anthropic-compatible interface)."""
        return AsyncBobMessages(self.client, **kwargs)

# Made with Bob
