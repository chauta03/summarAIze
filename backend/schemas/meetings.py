from pydantic import BaseModel, ConfigDict


class Meeting(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    type: str
    meeting_id: str
    meeting_url: str
