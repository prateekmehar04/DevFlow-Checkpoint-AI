import json
from typing import Any, Dict, Optional

from .ibm_bob_client import AsyncIBMBobClient
from ...config import settings


class TestingAgent:
    """Testing agent that uses IBM BOB to generate tests."""
    
    def __init__(self, client: Optional[AsyncIBMBobClient] = None):
        self.client = client or AsyncIBMBobClient(api_key=settings.ibm_bob_api_key)
    
    async def run(self, code: str, test_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate test cases and test code using IBM BOB.
        
        Args:
            code: The code to test
            test_type: Type of tests (unit, integration, e2e)
            context: Additional context
            
        Returns:
            Dictionary containing test cases, test code, and fixtures
        """
        # Check if API key is configured
        if not settings.ibm_bob_api_key or settings.ibm_bob_api_key == "your-ibm-bob-api-key-here":
            return self._fallback_response(code, test_type, context)
        
        system_prompt = """You are IBM BOB, a testing expert. Your role is to:

1. Generate comprehensive test cases
2. Write actual test code (pytest format)
3. Create test data fixtures
4. Cover happy paths, edge cases, and error scenarios
5. Include clear assertions and expected outcomes

Always structure your response as valid JSON with the following format:
{
    "agent": "testing",
    "mode": "ibm-bob",
    "test_type": "unit|integration|e2e",
    "test_cases": [
        {
            "name": "test case name",
            "description": "what it tests",
            "scenario": "test scenario"
        }
    ],
    "test_code": "Complete pytest test code",
    "fixtures": "Test fixtures and data",
    "coverage_notes": "What is covered"
}"""
        
        user_prompt = f"""Code to test:
```
{code[:2000]}  # Limit code length
```

Test Type: {test_type}

Context:
{json.dumps(context, indent=2)}

Please generate:
1. Comprehensive test cases covering happy paths, edge cases, and errors
2. Actual pytest test code
3. Test fixtures and data
4. Assertions and expected outcomes

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
                test_data = json.loads(content)
                test_data.setdefault("agent", "testing")
                test_data.setdefault("mode", "ibm-bob")
                test_data.setdefault("test_type", test_type)
                test_data.setdefault("code_excerpt", code[:500])
                return test_data
            except json.JSONDecodeError:
                return {
                    "agent": "testing",
                    "mode": "ibm-bob",
                    "test_type": test_type,
                    "raw_response": content,
                    "code_excerpt": code[:500]
                }
                
        except Exception as e:
            return {
                "agent": "testing",
                "mode": "ibm-bob-error",
                "error": str(e),
                "test_type": test_type,
                "fallback": self._fallback_response(code, test_type, context)
            }
    
    def _fallback_response(self, code: str, test_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback response when API is not configured."""
        return {
            "agent": "testing",
            "mode": "fallback",
            "test_type": test_type,
            "summary": "Using fallback testing (configure IBM_BOB_API_KEY for IBM BOB)",
            "recommended_cases": [
                "Create a project and assert the response includes id and timestamps.",
                "Create two checkpoints and assert diff reports changed fields.",
                "Transition plan to code and assert an automatic checkpoint is created.",
                "Reject invalid workflow transitions with HTTP 409.",
                "Rollback a workflow and assert context is restored from checkpoint state.",
            ],
            "pytest_hint": "Use FastAPI TestClient with async database session for testing.",
            "context_keys": sorted(context.keys()),
            "code_excerpt": code[:500],
        }
