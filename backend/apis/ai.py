import asyncio
import os
import tempfile

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
from services.ai import geminiAgent
from moviepy.video.io.VideoFileClip import VideoFileClip
from services.ai.prompt import SUMMARIZATION_PROMPT

router = APIRouter()
agent = geminiAgent.GeminiAgent()

async def continuous_transcription(audio_path: str, duration_sec: int) -> str:
    """
    Uses Azure continuous recognition to transcribe the audio.
    Waits for (duration_sec + buffer) seconds before stopping recognition.
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_REGION")
    if not speech_key or not region:
        raise Exception("Azure Speech key or region not provided.")
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    audio_config = speechsdk.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    transcript_parts = []

    def recognized_callback(evt):
        # Append recognized text from each result.
        transcript_parts.append(evt.result.text)
        print("Intermediate result:", evt.result.text)
    
    recognizer.recognized.connect(recognized_callback)
    
    recognizer.start_continuous_recognition()
    # Wait for the entire duration plus a buffer (e.g., 10 seconds).
    await asyncio.sleep(duration_sec + 10)
    recognizer.stop_continuous_recognition()
    
    return " ".join(transcript_parts)

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        print("Received file:", file.filename)
        # Step 1: Save uploaded file to a temporary file.
        suffix = f".{file.filename.split('.')[-1]}"
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        contents = await file.read()
        temp_file.write(contents)
        temp_file.flush()
        print("File saved to temporary location:", temp_file.name)

        # Step 2: Determine if the file is a video and extract audio if needed.
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext in ["mp4", "mov", "avi", "mkv"]:
            print("Video file detected, extracting audio using moviepy...")
            audio_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            video_clip = VideoFileClip(temp_file.name)
            if video_clip.audio is None:
                video_clip.close()
                return JSONResponse(status_code=400, content={"error": "No audio track found in the video."})
            video_clip.audio.write_audiofile(audio_temp.name, codec='pcm_s16le')
            video_clip.close()
            audio_path = audio_temp.name
            print("Audio extracted to:", audio_path)
        else:
            audio_path = temp_file.name

        # Step 3: Load audio with pydub to get duration.
        try:
            print("Attempting to load audio with pydub...")
            audio = AudioSegment.from_file(audio_path)
            duration_sec = round(len(audio) / 1000)
            duration_str = f"{duration_sec // 60}:{duration_sec % 60:02d} min"
            print("Audio loaded successfully. Duration:", duration_str)
        except Exception as e:
            print("Error in loading audio:", e)
            # Default to 60 seconds if loading fails.
            duration_sec = 60
            duration_str = "Unknown"

        # Step 4: Convert the audio to WAV for Azure Speech API if necessary.
        try:
            if not audio_path.endswith(".wav"):
                converted_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
                audio.export(converted_temp.name, format="wav")
                converted_temp.flush()
                final_audio_path = converted_temp.name
            else:
                final_audio_path = audio_path
            print("Audio ready for Azure Speech API:", final_audio_path)
        except Exception as e:
            print("Error converting audio to WAV:", e)
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to prepare audio for transcription."}
            )

        # Step 5: Use Azure Speech-to-Text with continuous recognition to generate transcript.
        try:
            transcript = await continuous_transcription(final_audio_path, duration_sec)
            if not transcript:
                transcript = "Speech could not be recognized."
            print("Azure continuous speech recognition complete:", transcript)
        except Exception as e:
            print("Error in Azure speech recognition:", e)
            transcript = "Error in Azure speech recognition."

        # Step 6: Generate summary using Gemini Agent.
        try:
            print("Generating summary using GeminiAgent...")
            summary = agent.generateSumary(transcript, prompt=SUMMARIZATION_PROMPT)
            print("Summary generated successfully.")
        except Exception as e:
            print("Error in generating summary:", e)
            summary = "Error generating summary"

        return {
            "transcript": transcript,
            "summary": summary,
            "duration": duration_str
        }

    except Exception as e:
        print("General error in upload_audio:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})
