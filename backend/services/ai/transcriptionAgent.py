import azure.cognitiveservices.speech as speechsdk
import os
import subprocess
import uuid
import requests
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException


class TranscriptionAgent:
    """
    A class to represent a transcript.
    """

    def __init__(self):
        """
        Initialize the Transcript with the given text.
        """
        self.client = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_REGION"))
        
    def _get_media_duration(self, file_path: str) -> float:
        """
        Gets the duration of an audio or video file in seconds.
        """
        command = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            return float(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Failed to get media duration: {e.stderr.strip()}")
    
    def extract_audio(self, video_path: str) -> str:
        """Extracts audio from video and saves it as a .wav file."""
        audio_path = f"/tmp/{uuid.uuid4()}.wav"  # Generate a unique filename

        command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"]
        video_duration = int(self._get_media_duration(video_path))
        try:
            subprocess.run(command, check=True)
            return {
                "path": audio_path,
                "duration": video_duration,
                }
        except subprocess.CalledProcessError:
            raise HTTPException(status_code=500, detail="Failed to extract audio from video")


    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribes speech from an audio file using Azure Speech-to-Text."""
        
        audio_config = speechsdk.AudioConfig(filename=audio_path)

        recognizer = speechsdk.SpeechRecognizer(speech_config=self.client, audio_config=audio_config)
        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized"
        elif result.reason == speechsdk.ResultReason.Canceled:
            return f"Speech recognition canceled: {result.cancellation_details.reason}"
        

    async def transcribe_video(self, file: UploadFile = None, video_path: str = None):
        """
        Accepts a video file or a video URI, extracts audio, transcribes it, and returns the transcription.
        """
        if not file and not video_path:
            raise HTTPException(status_code=400, detail="Either a file or a video URI must be provided.")

        temp_video_path = None
        try:
            if file:
                temp_video_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
                with open(temp_video_path, "wb") as buffer:
                    buffer.write(await file.read())
                video_path = temp_video_path
            
            # Verify file integrity before processing
            if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
                raise HTTPException(status_code=400, detail="Uploaded video file is empty or missing.")

            # Extract audio
            audio_info = self.extract_audio(video_path)
            
            if not os.path.exists(audio_info["path"]) or os.path.getsize(audio_info["path"]) == 0:
                raise HTTPException(status_code=500, detail="Extracted audio file is empty or corrupted.")

            # Transcribe audio
            transcription = self.transcribe_audio(audio_info["path"])
            
            return {
                "transcription": transcription,
                "duration": audio_info["duration"]
            }
        finally:
            # Clean up files
            if temp_video_path and os.path.exists(temp_video_path):
                os.remove(temp_video_path)
            if "audio_info" in locals() and os.path.exists(audio_info["path"]):
                os.remove(audio_info["path"])
