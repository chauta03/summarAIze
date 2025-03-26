from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from services.ai import geminiAgent
from crud import meetings
from db.db_manager import DBSessionDep
from schemas.meetings import Meeting
import os
import azure.cognitiveservices.speech as speechsdk
import subprocess
import uuid

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

def extract_audio(video_path: str) -> str:
    """Extracts audio from video and saves it as a .wav file."""
    audio_path = f"/tmp/{uuid.uuid4()}.wav"  # Generate a unique filename

    command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"]
    try:
        subprocess.run(command, check=True)
        return audio_path
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Failed to extract audio from video")

def transcribe_audio(audio_path: str) -> str:
    """Transcribes speech from an audio file using Azure Speech-to-Text."""
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_REGION"))
    audio_config = speechsdk.AudioConfig(filename=audio_path)

    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized"
    elif result.reason == speechsdk.ResultReason.Canceled:
        return f"Speech recognition canceled: {result.cancellation_details.reason}"

@router.post("/transcribe_video")
async def transcribe_video(file: UploadFile = File(...)):
    """Accepts a video file, extracts audio, transcribes it, and returns the transcription."""
    video_path = f"/tmp/{file.filename}"
    
    # Save uploaded file
    with open(video_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract audio
    audio_path = extract_audio(video_path)

    # Transcribe audio
    transcription = transcribe_audio(audio_path)

    # Clean up files
    os.remove(video_path)
    os.remove(audio_path)

    return {"transcription": transcription}