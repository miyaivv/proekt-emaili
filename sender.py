import base64
import os

from email.mime.text import MIMEText

from google.auth.transport.requests import Requests
from  google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Sender:
    def __init__(self):
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        self.service = self.gmail_service()

    def gmail_service(self):
      '''flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
      creds = flow.run_local_server(port=0)
      return build("gmail", "v1", credentials=creds)'''

      credentials_path = os.environ.get("CREDENTIALS_PATH", "credentials.json")
      token_path = os.environ.get( "TOKEN_PATH", "token.json")
      creds = None

      if os.path.exists(token_path):
         creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

      if creds and creds.expired and creds.refresh_token:
         creds.refresh(Requests())

      elif not creds or not creds.valid:
         flow = InstalledAppFlow.from_client_secret_file(credentials_path, self.SCOPES)
         creds = flow.run_local_server(port=0)

      if os.environ.get("SAVE_TOKEN") == "true":
         with open(token_path, "w") as token:
            token.write(creds.to_json())

      return build("gmail", "v1", credentials=creds)

    def send_email(self, service, to, subject, body):
      message = MIMEText(body,'plain', 'utf-8')
      message["to"] = to
      message["subject"] = subject

      encoded = base64.urlsafe_b64encode( message.as_bytes()).decode()

      service.users().messages().send(
        userId="me",
        body={"raw": encoded}
        ).execute()