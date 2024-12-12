import os
import csv
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from twilio.rest import Client

# Load environment variables from Heroku Config Vars
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
app = Flask(__name__)

class VoiceBroadcaster:
    """
    A class to send a voice broadcast to a list of contacts using Twilio.
    """
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        """
        Initialize the VoiceBroadcaster with Twilio credentials.
        """
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number
    
    def send_voice_broadcast(self, contacts: list, message_url: str):
        call_responses = []
        for contact in contacts:
            try:
                print(f"Attempting to call {contact} from {self.from_number} using URL: {message_url}")
                call = self.client.calls.create(
                    to=contact,
                    from_=self.from_number,
                    url=message_url
                )
                call_responses.append({
                    'to': contact,
                    'status': call.status,
                    'sid': call.sid
                })
                print(f"Call initiated to {contact} - Status: {call.status} - Call SID: {call.sid}")
            except Exception as e:
                call_responses.append({
                    'to': contact,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"Failed to call {contact} - Error: {str(e)}")
        return call_responses

    def load_contacts_from_csv(self, file_path: str) -> list:
        contacts = []
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and len(row) > 0:
                        phone_number = row[0].strip()  # Assuming phone numbers are in the 1st column
                        if not phone_number.startswith('+'):
                            phone_number = '+1' + phone_number  # Automatically add +1 for US numbers
                        contacts.append(phone_number)
        except Exception as e:
            print(f"Error loading contacts from {file_path}: {str(e)}")
        return contacts


@app.route('/')
def upload_form():
    """
    Renders the form to upload the CSV file and submit the public URL.
    """
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles the form submission for the CSV file and audio URL.
    """
    if 'file' not in request.files:
        return 'No CSV file part'

    file = request.files['file']
    from_number = request.form.get('from_number')
    audio_url = request.form.get('audio_url')
    
    if not from_number:
        return 'No "From" phone number specified'
    
    if not audio_url or not audio_url.startswith('http'):
        return 'Invalid audio URL. Please provide a valid public URL (e.g., https://example.com/audio.mp3).'
    
    if file.filename == '':
        return 'No selected CSV file'
    
    if file:
        csv_filename = secure_filename(file.filename)
        csv_path = os.path.join('/tmp', csv_filename)  # Store temporarily in /tmp
        file.save(csv_path)
        
        broadcaster = VoiceBroadcaster(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, from_number)
        contacts = broadcaster.load_contacts_from_csv(csv_path)
        
        results = broadcaster.send_voice_broadcast(contacts, audio_url)
        
        return f"Broadcast sent successfully to {len(contacts)} contacts."
    else:
        return 'Invalid file type. Please upload a CSV file.'


if __name__ == "__main__":
    app.run(debug=True)
