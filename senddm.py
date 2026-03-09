from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")          # put in .env
recipient = os.getenv("RECIPIENT")  # username like "girlfriend_username" or numeric ID

def send(audio_path: str):
    with TelegramClient("session", api_id, api_hash) as client:
        # Authorize if needed (only first run)
        if not client.is_user_authorized():
            client.send_code_request(phone)
            client.sign_in(phone, input("Enter OTP: "))

        client.send_file(
            "me",
            audio_path,
            voice_note=True,
            caption="🌸 আজকের বার্তা"
        )
        print(f"✅ Sent: {audio_path}")