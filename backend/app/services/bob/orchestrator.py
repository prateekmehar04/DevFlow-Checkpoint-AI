from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncGenerator, Dict

from .ibm_bob_client import AsyncIBMBobClient
from ...config import settings
from .context_manager import ContextManager
from .debugging_agent import DebuggingAgent
from .planning_agent import PlanningAgent
from .testing_agent import TestingAgent


class BOBOrchestrator:
    """
    Main orchestrator for IBM BOB AI agents.
    Coordinates planning, debugging, and testing agents with context management.
    """
    
    def __init__(self) -> None:
        self.client = AsyncIBMBobClient(api_key=settings.ibm_bob_api_key) if settings.ibm_bob_api_key else None
        self.context_manager = ContextManager()
        self.planning_agent = PlanningAgent(self.client)
        self.debugging_agent = DebuggingAgent(self.client)
        self.testing_agent = TestingAgent(self.client)

    async def plan_milestones(self, project_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate project milestones using planning agent."""
        return await self.planning_agent.run(project_description, context)

    async def debug_code(self, code: str, error: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and debug code errors using debugging agent."""
        return await self.debugging_agent.run(code, error, context)

    async def generate_tests(self, code: str, test_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test cases using testing agent."""
        return await self.testing_agent.run(code, test_type, context)

    async def maintain_context(self, workflow_id: str, new_data: Dict[str, Any]) -> None:
        """Update and persist workflow context."""
        existing = await self.context_manager.load_context(workflow_id)
        merged = self.context_manager.merge_contexts(existing, new_data)
        await self.context_manager.save_context(workflow_id, merged)

    async def stream_response(self, prompt: str, context: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """
        Stream AI responses in real-time using IBM BOB.
        
        Args:
            prompt: User prompt
            context: Workflow context
            
        Yields:
            Server-sent event formatted strings
        """
        # Check if API key is configured
        if not self.client or not settings.ibm_bob_api_key or settings.ibm_bob_api_key == "your-ibm-bob-api-key-here":
            # Fallback streaming
            parts = [
                "BOB checkpoint received (fallback mode - configure IBM_BOB_API_KEY).",
                f"Context keys: {', '.join(sorted(context.keys())) or 'none'}.",
                f"Next action: {prompt[:120]}",
            ]
            for part in parts:
                await asyncio.sleep(0.05)
                yield f"data: {part}\n\n"
            return
        
        # Build system prompt with context
        system_prompt = self._build_system_prompt(context)
        
        try:
            # Stream from IBM BOB
            async with self.client.stream(
                model=settings.bob_model,
                max_tokens=settings.bob_max_tokens,
                temperature=settings.bob_temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            ) as stream:
                async for text in stream.text_stream:
                    yield f"data: {text}\n\n"
        except Exception as e:
            yield f"data: Error streaming from BOB: {str(e)}\n\n"
    
    def _build_system_prompt(self, context: Dict[str, Any]) -> str:
        """Build system prompt with context information."""
        context_summary = json.dumps(context, indent=2) if context else "No context available"
        
        return f"""You are IBM BOB, an AI software architect and development assistant for DevFlow Checkpoint AI.

Current Context:
{context_summary}

Your role:
- Provide clear, actionable guidance
- Break down complex tasks into steps
- Maintain awareness of the project's checkpoint-based workflow
- Help with planning, debugging, and testing
- Be concise but thorough

Always consider the current workflow state and previous checkpoints when providing guidance."""
