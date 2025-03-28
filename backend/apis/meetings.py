from io import BytesIO
from fastapi import APIRouter, Depends, File, UploadFile
from crud import meetings
from db.db_manager import DBSessionDep
from schemas.meetings import Meeting
from apis.sessions import get_current_user
from db.models import User
from services.meetings.azure_blob_storage import StorageService
from services.ai import transcriptionAgent
from services.ai import geminiAgent
import os
from fastapi import HTTPException

router = APIRouter()
storage_service = StorageService()
agent = geminiAgent.GeminiAgent()
transcription_agent = transcriptionAgent.TranscriptionAgent()


@router.post(
    "/create_google_meeting",
    response_model=Meeting
)
async def create_google_meeting(
    db_session: DBSessionDep,
    current_user: User = Depends(get_current_user),
):
    res  = await meetings.create_google_meeting(db_session, current_user.id)
    return res

@router.get(
    "/meetings-list",
    response_model=list[Meeting]
)
async def get_user_meetings(
    db_session: DBSessionDep,
    current_user: User = Depends(get_current_user),
):

    return await meetings.list_user_meetings(db_session, current_user.id)

@router.get("/meeting_summary/{meeting_id}")
async def get_meeting_summary(
    meeting_id: str,
    db_session: DBSessionDep,
    current_user: User = Depends(get_current_user),
):
    return await meetings.get_meeting_summary(
        meeting_id=meeting_id,
        db_session=db_session,
        user_id=current_user.id
        )

@router.post("/upload_video_to_azure")
async def upload_video(file: UploadFile = File(...)):
    """Upload a video file to Azure Blob Storage."""
    storage_service = StorageService()
    file_content = await file.read()
    return await storage_service.upload_video(file, file_content)

@router.get("/list_videos")
async def list_videos():
    """List all videos in Azure Blob Storage."""
    storage_service = StorageService()
    return storage_service.list_videos()

@router.delete("/delete_video/{filename}")
async def delete_video(filename: str):
    """Delete a video file from Azure Blob Storage."""
    storage_service = StorageService()
    return storage_service.delete_video(filename)

@router.get("/get_video/{filename}")
async def get_video(filename: str):
    """Get a video file from Azure Blob Storage."""
    storage_service = StorageService()
    return storage_service.get_video(filename)


@router.post("/upload_meeting_recording")
async def upload_meeting_recording(
    db_session: DBSessionDep,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """Upload a meeting recording to Azure Blob Storage."""
    azure_key = os.getenv("AZURE_SPEECH_KEY")
    azure_region = os.getenv("AZURE_REGION")
    if not azure_key or not azure_region:
        raise HTTPException(status_code=500, detail="Azure credentials not set in environment variables")

    # Read the file content only once
    file_content = await file.read()
    
    # Ensure the file is not empty
    if not file_content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Reset file pointer for further reading
    file.file.seek(0)

    # Upload the video
    upload_response = await storage_service.upload_video(file, file_content)
    if not upload_response or 'video_url' not in upload_response or 'created_at' not in upload_response:
        raise HTTPException(status_code=500, detail="Failed to upload video to Azure Blob Storage")
    
    meeting_url = upload_response["video_url"]
    created_at = upload_response["created_at"]

    try:
        # Transcribe video and generate summary
        transcription_info = await transcription_agent.transcribe_video(file)
        transcription_info["summary"] = agent.generateSummary(transcription_info["transcription"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


    # Save the meeting recording information to the database
    # try:
    #     await meetings.save_meeting_recording(
    #         db_session, 
    #         current_user.id, 
    #         "upload", 
    #         meeting_url, 
    #         None, 
    #         transcription_info["transcription"], 
    #         transcription_info["summary"], 
    #         transcription_info["duration"], 
    #         created_at
    #     )
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error saving meeting recording: {str(e)}")
        
    return {
        "message": "Meeting recording uploaded successfully",
        "video_url": meeting_url,
        "transcription": transcription_info["transcription"],
        "summary": transcription_info["summary"],
        "duration": transcription_info["duration"],
        "created_at": created_at
    }
