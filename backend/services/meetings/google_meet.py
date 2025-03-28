import os.path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import requests
from db.models import AppIntegration, Meeting
from services.ai import transcriptionAgent, geminiAgent

SCOPES = ['https://www.googleapis.com/auth/meetings.space.created', "https://www.googleapis.com/auth/drive"]
load_dotenv()

class GoogleMeetServices:
    def __init__(self, db_session: AsyncSession, user_id: int):
        self.db_session = db_session
        self.user_id = user_id
        
        
    async def get_credentials(self):
        # Query the AppIntegration table for Google Meet credentials
        result = await self.db_session.execute(
            select(AppIntegration).where(
                AppIntegration.user_id == self.user_id,
                AppIntegration.app_name == "google_meet"
            )
        )
        app_integration = result.scalars().first()
        creds = None
        if app_integration:
            user_info = {
                "token": app_integration.token,
                "refresh_token": app_integration.refresh_token,
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"), 
                "scopes": SCOPES,
                "universe_domain": "googleapis.com",
                "account": "",
                "expiry": app_integration.expire.isoformat()
            }
            creds = Credentials.from_authorized_user_info(user_info, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                app_integration.token = creds.token
                app_integration.expire = creds.expiry
                self.db_session.add(app_integration)
                await self.db_session.commit()
            else:
                print("create new authorization token")
                return await self.authorize()
        return creds

    async def create_google_meet(self):
        creds = await self.get_credentials()
        if not creds:
            return None
        try:
            client = meet_v2.SpacesServiceClient(credentials=creds)
            request = meet_v2.CreateSpaceRequest()
            response = client.create_space(request=request)
            print(response)
            print(f'Space created: {response.meeting_uri}')
        except Exception as error:
            print(f'An error occurred: {error}')
        return {
            "meeting_uri": response.meeting_uri,
            "meeting_id": response.name.split("/")[1]
        }
    
    async def authorize(self):
        client_config = {
            "web":{
                "client_id":os.getenv("GOOGLE_CLIENT_ID"),
                "project_id":os.getenv("GOOGLE_PROJECT_ID"),
                "auth_uri":"https://accounts.google.com/o/oauth2/auth",
                "token_uri":"https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                "client_secret":os.getenv("GOOGLE_CLIENT_SECRET")
            }
        }
        flow = InstalledAppFlow.from_client_config(client_config=client_config, scopes=SCOPES)
        creds = flow.run_local_server(port=0, prompt="consent")
        # with open(self.token_path, 'w') as token:
        #     token.write(creds.to_json())
        app_integration = AppIntegration(
            user_id=self.user_id,
            app_name="google_meet",
            token=creds.token,
            refresh_token=creds.refresh_token,
            expire=creds.expiry
        )
        self.db_session.add(app_integration)
        await self.db_session.commit()

        return creds
    
    async def unauthorize(self):
        result = await self.db_session.execute(
            select(AppIntegration).where(
                AppIntegration.user_id == self.user_id,
                AppIntegration.app_name == "google_meet"
            )
        )
        app_integration = result.scalars().first()

        if app_integration:
            await self.db_session.delete(app_integration)
            await self.db_session.commit()

        return True

    async def get_conferences(self, meeting_id:str):
        creds = await self.get_credentials()
        result = []
        if not creds:
            return None
        try:
            client = meet_v2.ConferenceRecordsServiceAsyncClient(credentials=creds)

            # Initialize request argument(s)
            request = meet_v2.ListConferenceRecordsRequest(
                filter=f"space.name = spaces/{meeting_id}"
            )

            # Make the request
            page_result = await client.list_conference_records(request=request)
        
            # Handle the response
            async for response in page_result:
                result.append(response)
        except Exception as error:
            print(f'An error occurred: {error}')
            
        return result
    
    async def get_recording(self, meeting_id: str):
        conferences = await self.get_conferences(meeting_id=meeting_id)
        if len(conferences) == 0:
            return None
        recent_conference_name = conferences[0].name
        creds = await self.get_credentials()
        records = []
        if not creds:
            return None
        try:
            client = meet_v2.ConferenceRecordsServiceAsyncClient(credentials=creds)
            request = meet_v2.ListRecordingsRequest(
                parent=recent_conference_name,
            )

            # Make the request
            page_result = await client.list_recordings(request=request)
            # Handle the response
            async for response in page_result:
                records.append(response)
            print(records)

        except Exception as error:
            print(f'An error occurred: {error}')
        if len(records) == 0:
            return None

        # Get the Google Drive file ID from the export URI
        drive_file = records[0].drive_destination
        file_id = drive_file.file

        # Download the file using Google Drive API
        video_path = await self.download_drive_file(file_id, creds)
        return video_path

    async def download_drive_file(self, file_id: str, creds) -> str:
        """
        Downloads a file from Google Drive using the file ID.
        """
        try:
            # Initialize the Google Drive API client
            drive_service = build('drive', 'v3', credentials=creds)

            # Get the file metadata
            file_metadata = drive_service.files().get(fileId=file_id).execute()
            print("+++++++++File Data+++++++")
            print(file_metadata)
            file_name = file_metadata['name']

            # Download the file content
            request = drive_service.files().get_media(fileId=file_id)
            video_path = f"/tmp/{file_name}"
            with open(video_path, "wb") as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Download progress: {int(status.progress() * 100)}%")

            return video_path
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise HTTPException(status_code=500, detail=f"Failed to download video from Google Drive: {error}")

    async def summarize_meeting(self, meeting_id: str):
        """
        Summarizes a Google Meet meeting by transcribing the recording and generating a summary.
        """
        record_uri = await self.get_recording(meeting_id=meeting_id)
        if not record_uri:
            return None

        transcriptAgent = transcriptionAgent.TranscriptionAgent()
        summaryAgent = geminiAgent.GeminiAgent()

        try:
            # Transcribe the video
            record_transcription = await transcriptAgent.transcribe_video(video_path=record_uri)
            print("=====")
            print("transcript: ", record_transcription)
            # Generate the summary
            record_transcription["summary"] = summaryAgent.generateSummary(record_transcription["transcription"])

            return record_transcription
        finally:
            # Clean up the temporary downloaded file
            if os.path.exists(record_uri):
                os.remove(record_uri)




