import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/meetings.space.created']

class GoogleMeetServices:
    def __init__(self):
        self.token_path = "token.json"
        self.creds_path = "credential.json"
        
    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # later phrase: if no creadential, re direct to an authorization page
                print("create new authorization token")
                return self.authorize()
        return creds
    def create_google_meet(self):
        creds = self.get_credentials()
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
    def authorize(self):
        flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(self.token_path, 'w') as token:
            token.write(creds.to_json())
        return creds
    
    def unauthorize(self):
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
        return True
