from pydantic import BaseModel, ConfigDict


class Meeting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    type: str
    meeting_id: str | None = None
    meeting_url: str | None = None
    record_url: str | None = None
    transcription: str | None = None
    summary: str | None = None
    duration: int | None = None
