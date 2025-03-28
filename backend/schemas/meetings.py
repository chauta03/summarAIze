from pydantic import BaseModel, ConfigDict


class Meeting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    type: str
    meeting_id: str | None = None
    meeting_url: str
    transcription: str | None = None
    summary: str | None = None
    duration: str | None = None
    created_at: str | None = None
