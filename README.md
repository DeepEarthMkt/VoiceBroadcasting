# Voice Broadcast Application
# Developed by Logan Artrip 12/12/2024

# Features
# - Upload a CSV file with phone numbers.
# - Submit a public URL for an MP3 or WAV file.
# - Uses Twilio Voice API to make calls and play the audio.
# - View call logs via Heroku.

# Requirements
# - Twilio Account
# - Heroku Account
# - Twilio Verified Number

# Folder Structure
# - app.py: Main application logic
# - templates/upload.html: Form for uploading CSV and URL
# - requirements.txt: Python dependencies
# - runtime.txt: Python version
# - Procfile: Heroku process instructions

# Environment Variables
# - TWILIO_ACCOUNT_SID: Twilio Account SID (Set in Heroku Config Vars)
# - TWILIO_AUTH_TOKEN: Twilio Auth Token (Set in Heroku Config Vars)
# - TWILIO_PHONE_NUMBER: Twilio phone number (E.164 format) (Set in Heroku Config Vars)

# Usage Instructions (Heroku Dashboard)
# 1. Access Heroku Dashboard
#    - Go to https://dashboard.heroku.com/
#    - Click on the app you created.

# 2. Upload CSV File and Audio URL
#    - On the app's web page, you will see a form.
#    - Upload a CSV file containing the phone numbers (E.164 format, e.g., +1234567890).
#    - Enter your Twilio verified phone number in the "From" phone number field.

# Creating a Public Audio Link Using TwiML BIN

# How to Use TwiML Bin

# 1. Access Twilio Console
#    - Go to https://www.twilio.com/console/voice/twiml-bins

# 2. Create a New TwiML Bin
#    - Click the "Create New TwiML Bin" button.
#    - Give it a descriptive name (e.g., "Voice Broadcast Audio").
#    - In the TwiML Content section, add the following XML:
#      <Response>
#        <Play>https://your-public-audio-url.com/audio.mp3</Play>
#      </Response>
#    - Click "Create" to save the TwiML Bin.

# 3. Copy the TwiML Bin URL
#    - After saving, you will see a URL at the top of the TwiML Bin page.
#    - It will look like this: 
#      https://handler.twilio.com/twiml/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# 4. Use the TwiML Bin URL in the App
#    - Instead of using a public URL directly, use the TwiML Bin URL in the "audio URL" input of the form.
#    - This URL will provide the instructions to Twilio to play the audio file during the call.

# 3. Submit the Form
#    - Click the submit button.
#    - The system will process the CSV file and start calls to each phone number listed in the CSV.

# 4. Track Call Progress
#    - Open Heroku Dashboard.
#    - Click on the app, then click More > View Logs.
#    - Look for log entries like:
#      "Attempting to call +12345678900 from +19876543210 using URL: https://example.com/audio.mp3"
#      "Call initiated to +12345678900 - Status: queued - Call SID: CAxxxxxxxxxxxxxxxxxxxxx"

# 5. Check Twilio Dashboard
#    - Go to https://www.twilio.com/console/voice/logs.
#    - Look for the status of calls made (queued, in-progress, failed, etc.).

# CSV File Format
# - Single column with phone numbers in E.164 format
# - Example CSV content:
#   +12345678901
#   +11234567890
#   +16505551234

# How Calls Work
# - Call request is sent to Twilio for each phone number.
# - Twilio fetches the audio file from the URL provided.
# - Twilio plays the audio file for the recipient.

# Common Issues and Fixes
# - No call received: Check that your Twilio phone number is verified.
# - Application error occurred: Ensure the audio URL is valid and publicly accessible.
# - File not found: Ensure the URL points to a valid MP3 or WAV file.
# - Twilio 400 error: Ensure phone numbers are in E.164 format (e.g., +1234567890).

# Testing Tips
# - Use public URLs from AWS S3, Dropbox, or Google Drive.
# - Example test URL: https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3

# License
# - Licensed under MIT License

# Contributing
# 1. Fork the repo.
# 2. Create a new branch for changes.
# 3. Commit and push changes.
# 4. Open a pull request.

# Contact
# - Reach out via GitHub Issues or email at logan@deepearthmkt.com
