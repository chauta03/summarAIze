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
    
    def extract_audio(self, video_path: str) -> str:
        """Extracts audio from video and saves it as a .wav file."""
        audio_path = f"/tmp/{uuid.uuid4()}.wav"  # Generate a unique filename

        command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"]
        try:
            subprocess.run(command, check=True)
            return audio_path
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
        

    async def transcribe_video(self, file: UploadFile = None, video_path: str = None) -> str:
        """
        Accepts a video file or a video URI, extracts audio, transcribes it, and returns the transcription.
        """
        if not file and not video_path:
            raise HTTPException(status_code=400, detail="Either a file or a video URI must be provided.")

        # Determine the video source
        if file:
            # Save the uploaded file
            video_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
            with open(video_path, "wb") as buffer:
                buffer.write(await file.read())

        try:
            # Extract audio
            audio_path = self.extract_audio(video_path)

            # Transcribe audio
            transcription = self.transcribe_audio(audio_path)

            return transcription
        finally:
            # Clean up files
            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)