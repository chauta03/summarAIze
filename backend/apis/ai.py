from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from pydub import AudioSegment
import tempfile
from services.ai import geminiAgent

router = APIRouter()
agent = geminiAgent.GeminiAgent()

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    try:
        print("Received file:", file.filename)
        # Step 1: Save uploaded file
        suffix = f".{file.filename.split('.')[-1]}"
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        contents = await file.read()
        temp.write(contents)
        temp.flush()
        print("File saved to temporary location:", temp.name)

        # Step 2: Get duration using pydub
        try:
            print("Attempting to load audio with pydub...")
            audio = AudioSegment.from_file(temp.name)
            duration_sec = round(len(audio) / 1000)
            duration_str = f"{duration_sec // 60}:{duration_sec % 60:02d} min"
            print("Audio loaded successfully. Duration:", duration_str)
        except Exception as e:
            print("Error in loading audio:", e)
            duration_str = "Unknown"

        # Step 3: Prepare a default transcript (placeholder)
        transcript = """
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
        print("Transcript prepared.")

        # Step 4: Generate summary using Gemini Agent
        try:
            print("Generating summary using GeminiAgent...")
            summary = agent.generateSumary(transcript)
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
