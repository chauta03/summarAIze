import os.path
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from db.models import AppIntegration


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']
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
            print(f'Space created: {response.meeting_uri}')
        except Exception as error:
            print(f'An error occurred: {error}')
            
        return {
            "meeting_uri": response.meeting_uri,
            "meeting_id": response.meeting_code
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
        with open(self.token_path, 'w') as token:
            token.write(creds.to_json())
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
    
    def unauthorize(self):
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
        return True
