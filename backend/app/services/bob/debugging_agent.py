import json
from typing import Any, Dict, Optional

from .ibm_bob_client import AsyncIBMBobClient
from ...config import settings


class DebuggingAgent:
    """Debugging agent that uses IBM BOB to analyze errors."""
    
    def __init__(self, client: Optional[AsyncIBMBobClient] = None):
        self.client = client or AsyncIBMBobClient(api_key=settings.ibm_bob_api_key)
    
    async def run(self, code: str, error: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze code errors and provide solutions using IBM BOB.
        
        Args:
            code: The code that caused the error
            error: The error message
            context: Additional context
            
        Returns:
            Dictionary containing diagnosis, suggestions, and fixes
        """
        # Check if API key is configured
        if not settings.ibm_bob_api_key or settings.ibm_bob_api_key == "your-ibm-bob-api-key-here":
            return self._fallback_response(code, error, context)
        
        system_prompt = """You are IBM BOB, an expert debugging assistant. Your role is to:

1. Analyze code errors thoroughly
2. Identify root causes
3. Provide clear, step-by-step fix instructions
4. Suggest preventive measures
5. Include code examples when helpful

Always structure your response as valid JSON with the following format:
{
    "agent": "debugging",
    "mode": "ibm-bob",
    "diagnosis": "Root cause analysis",
    "suggestions": ["step 1", "step 2", "step 3"],
    "fixes": [
        {
            "description": "What to fix",
            "code": "Fixed code example"
        }
    ],
    "preventive_measures": ["measure 1", "measure 2"]
}"""
        
        user_prompt = f"""Code:
```
{code[:2000]}  # Limit code length
```

Error:
{error}

Context:
{json.dumps(context, indent=2)}

Please provide:
1. Root cause analysis
2. Step-by-step fix instructions
3. Code examples if applicable
4. Preventive measures

Return ONLY valid JSON, no additional text."""
        
        try:
            response = await self.client.create(
                model=settings.bob_model,
                max_tokens=settings.bob_max_tokens,
                temperature=settings.bob_temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            content = response.get("content", [{}])[0].get("text", "")
            
            try:
                debug_data = json.loads(content)
                debug_data.setdefault("agent", "debugging")
                debug_data.setdefault("mode", "ibm-bob")
                debug_data.setdefault("code_excerpt", code[:500])
                debug_data.setdefault("error", error)
                return debug_data
            except json.JSONDecodeError:
                return {
                    "agent": "debugging",
                    "mode": "ibm-bob",
                    "diagnosis": "BOB analyzed the error",
                    "raw_response": content,
                    "code_excerpt": code[:500],
                    "error": error
                }
                
        except Exception as e:
            return {
                "agent": "debugging",
                "mode": "ibm-bob-error",
                "error": str(e),
                "diagnosis": "Failed to analyze with BOB",
                "fallback": self._fallback_response(code, error, context)
            }
    
    def _fallback_response(self, code: str, error: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback response when API is not configured."""
        suggestions = [
            "Reproduce the failure with the smallest request or component state.",
            "Check that the active workflow state allows the attempted transition.",
            "Inspect checkpoint payload shape before persisting or restoring.",
        ]
        
        if "404" in error or "not found" in error.lower():
            suggestions.insert(0, "Verify that the project, checkpoint, or workflow id exists in storage.")
        if "422" in error or "validation" in error.lower():
            suggestions.insert(0, "Compare the request body against the Pydantic schema fields.")
        
        return {
            "agent": "debugging",
            "mode": "fallback",
            "diagnosis": "Using fallback debugging (configure IBM_BOB_API_KEY for IBM BOB)",
            "suggestions": suggestions,
            "context_keys": sorted(context.keys()),
            "code_excerpt": code[:500],
            "error": error,
        }
