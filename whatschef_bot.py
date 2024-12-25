from flask import Flask, request
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app: Flask = Flask(__name__)

# Fetch credentials from environment variables
TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")

if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_WHATSAPP_NUMBER:
    raise ValueError("Missing required environment variables for Twilio!")

# Initialize Twilio client
client: Client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route("/whatsapp", methods=["POST"])
def handleWhatsAppMessage() -> str:
    """
    Handle incoming WhatsApp messages and respond based on content.
    """
    incoming_message: str = request.form.get("Body", "").strip().lower()
    sender: str = request.form.get("From", "")

    print("Received message from %s: %s" % (sender, incoming_message))

    # Basic command handling
    if incoming_message == "menu":
        response_message: str = "Here is our menu: [Placeholder for menu details]"
    elif incoming_message == "help":
        response_message: str = "Type 'menu' to see our menu or 'help' for assistance."
    else:
        response_message: str = "Thank you! Your message has been recorded."

    # Send response
    client.messages.create(
        body=response_message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=sender
    )
