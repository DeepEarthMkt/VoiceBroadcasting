import os
import csv
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from twilio.rest import Client

# Load environment variables from Heroku Config Vars
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class VoiceBroadcaster:
    """
    A class to send a voice broadcast to a list of contacts using Twilio.
    """
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        """
        Initialize the VoiceBroadcaster with Twilio credentials.
        
        :param account_sid: Twilio Account SID
        :param auth_token: Twilio Auth Token
        :param from_number: Twilio phone number to send calls from
        """
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number
    
    def send_voice_broadcast(self, contacts: list, message_url: str):
        """
        Send a voice message to a list of contacts.
        
        :param contacts: List of phone numbers to call (must be E.164 format)
        :param message_url: URL to the TwiML or an audio file (MP3/WAV) for the message to be played
        """
        call_responses = []
        for contact in contacts:
            try:
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
                print(f"Call initiated to {contact} - Status: {call.status}")
            except Exception as e:
                call_responses.append({
                    'to': contact,
                    'status': 'failed',
                    'error': str(e)
                })
                print(f"Failed to call {contact} - Error: {str(e)}")
        
        return call_responses

    def load_contacts_from_csv(self, file_path: str) -> list:
        """
        Load contacts from a CSV file.
        
        :param file_path: Path to the CSV file containing the contacts.
        :return: List of phone numbers from the CSV file.
        """
        contacts = []
        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Check if the row is not empty
                        contacts.append(row[0])  # Assume phone numbers are in the first column
                print(f"Successfully loaded {len(contacts)} contacts from {file_path}")
        except Exception as e:
            print(f"Error loading contacts from {file_path}: {str(e)}")
        return contacts


def allowed_file(filename):
    """Check if the file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        broadcaster = VoiceBroadcaster(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)
        contacts = broadcaster.load_contacts_from_csv(file_path)
        message_url = "https://your-server-url.com/twiml.xml"
        results = broadcaster.send_voice_broadcast(contacts, message_url)
        return f"Broadcast sent successfully to {len(contacts)} contacts."
    else:
        return 'Invalid file type. Please upload a CSV file.'

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
