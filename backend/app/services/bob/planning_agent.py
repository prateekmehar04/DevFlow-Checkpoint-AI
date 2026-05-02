import json
from typing import Any, Dict, Optional

from .ibm_bob_client import AsyncIBMBobClient
from ...config import settings


class PlanningAgent:
    """Planning agent that uses IBM BOB to generate project plans."""
    
    def __init__(self, client: Optional[AsyncIBMBobClient] = None):
        self.client = client or AsyncIBMBobClient(api_key=settings.ibm_bob_api_key)
    
    async def run(self, project_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate project milestones and breakdown using IBM BOB.
        
        Args:
            project_description: Description of the project
            context: Additional context for planning
            
        Returns:
            Dictionary containing milestones, risks, and recommendations
        """
        # Check if API key is configured
        if not settings.ibm_bob_api_key or settings.ibm_bob_api_key == "your-ibm-bob-api-key-here":
            return self._fallback_response(project_description, context)
        
        system_prompt = """You are IBM BOB, an AI software architect specializing in breaking down
software projects into structured, checkpoint-based milestones. Your role is to:

1. Analyze project requirements thoroughly
2. Create 5-8 clear, actionable milestones
3. Define specific deliverables for each milestone
4. Identify potential risks and mitigation strategies
5. Recommend appropriate technology stack

Always structure your response as valid JSON with the following format:
{
    "agent": "planning",
    "mode": "ibm-bob",
    "summary": "Brief overview of the plan",
    "milestones": [
        {
            "name": "Milestone name",
            "goal": "Clear goal description",
            "deliverables": ["deliverable 1", "deliverable 2"],
            "estimated_effort": "time estimate"
        }
    ],
    "risks": ["risk 1", "risk 2"],
    "tech_recommendations": {
        "backend": "recommendation",
        "frontend": "recommendation",
        "database": "recommendation"
    }
}"""
        
        user_prompt = f"""Project Description:
{project_description}

Additional Context:
{json.dumps(context, indent=2)}

Please create a detailed project plan with structured milestones, deliverables, and risk assessment.
Return ONLY valid JSON, no additional text."""
        
        try:
            response = await self.client.create(
                model=settings.bob_model,
                max_tokens=settings.bob_max_tokens,
                temperature=settings.bob_temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            # Extract text content
            content = response.get("content", [{}])[0].get("text", "")
            
            # Try to parse as JSON
            try:
                plan_data = json.loads(content)
                # Ensure required fields
                plan_data.setdefault("agent", "planning")
                plan_data.setdefault("mode", "ibm-bob")
                plan_data.setdefault("input", project_description)
                return plan_data
            except json.JSONDecodeError:
                # If not valid JSON, wrap in structure
                return {
                    "agent": "planning",
                    "mode": "ibm-bob",
                    "summary": "BOB generated a detailed plan",
                    "raw_response": content,
                    "milestones": [],
                    "input": project_description
                }
                
        except Exception as e:
            return {
                "agent": "planning",
                "mode": "ibm-bob-error",
                "error": str(e),
                "summary": "Failed to generate plan with BOB",
                "fallback": self._fallback_response(project_description, context)
            }
    
    def _fallback_response(self, project_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback response when API is not configured."""
        focus = context.get("focus", "MVP demo")
        return {
            "agent": "planning",
            "mode": "fallback",
            "focus": focus,
            "summary": "Using fallback planning (configure IBM_BOB_API_KEY for IBM BOB)",
            "milestones": [
                {"name": "Foundation", "goal": "Create runnable backend and frontend shells"},
                {"name": "Checkpoint Core", "goal": "Persist snapshots, versions, restore, and diff"},
                {"name": "Workflow Engine", "goal": "Guide plan, code, debug, test states"},
                {"name": "BOB Integration", "goal": "Integrate real IBM BOB API calls"},
                {"name": "Testing & Polish", "goal": "Add tests, documentation, and deployment"},
            ],
            "risks": [
                "IBM_BOB_API_KEY not configured - using fallback responses",
                "Database migration from JSON to PostgreSQL needed",
            ],
            "input": project_description,
        }
