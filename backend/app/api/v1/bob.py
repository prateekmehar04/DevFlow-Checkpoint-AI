from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ...schemas.bob import BobChatRequest, BobDebugRequest, BobPlanRequest, BobTestRequest
from ...services.bob import BOBOrchestrator

router = APIRouter(prefix="/bob", tags=["bob"])
orchestrator = BOBOrchestrator()


@router.post("/plan")
def plan(payload: BobPlanRequest):
    return orchestrator.plan_milestones(payload.project_description, payload.context)


@router.post("/debug")
def debug(payload: BobDebugRequest):
    return orchestrator.debug_code(payload.code, payload.error, payload.context)


@router.post("/test")
def generate_tests(payload: BobTestRequest):
    return orchestrator.generate_tests(payload.code, payload.test_type, payload.context)


@router.post("/chat")
def chat(payload: BobChatRequest):
    if payload.workflow_id:
        orchestrator.maintain_context(payload.workflow_id, {"last_message": payload.message, **payload.context})
    return {
        "agent": "bob",
        "mode": "local-demo",
        "message": "I saved the current context and recommend creating a checkpoint before the next state change.",
        "next_steps": [
            "Create a checkpoint for the current milestone.",
            "Run the relevant tests for this state.",
            "Transition only after the checkpoint and tests are green.",
        ],
    }


@router.get("/stream")
async def stream(prompt: str, workflow_id: str = ""):
    context = orchestrator.context_manager.load_context(workflow_id) if workflow_id else {}
    return StreamingResponse(orchestrator.stream_response(prompt, context), media_type="text/event-stream")
