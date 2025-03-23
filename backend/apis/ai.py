from fastapi import APIRouter, Depends
from services.ai import geminiAgent
from crud import meetings
from db.db_manager import DBSessionDep
from schemas.meetings import Meeting

router = APIRouter()
agent = geminiAgent.GeminiAgent()

@router.get("/summary/{meeting_id}")
async def get_meeting_summary(meeting_id: str):
    sample_script = """
    Alex: Good morning, everyone. Let’s keep this short. Jamie, can you update us on the development progress?
    Jamie: Sure! The new login feature is almost complete. I just need to run a few more tests, and it should be ready for deployment by Friday.
    Alex: Great. Any blockers?
    Jamie: Not at the moment, but I may need some final UI tweaks from Sam.
    Alex: Sam, does that work for you?
    Sam: Yes, I can review it today and send any changes by tomorrow.
    Alex: Perfect. Anything else we need to discuss?
    Jamie: Nope, all good here.
    Sam: Same here.
    Alex: Alright, then. Thanks, everyone! Let’s touch base again next week."""
    summary = agent.generateSumary(sample_script)
    return {"meeting_id": meeting_id, "summary": summary}
