from telethon.sync import TelegramClient
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")          # put in .env
recipient = os.getenv("RECIPIENT")  # username like "girlfriend_username" or numeric ID

def send_voice(audio_path: str):
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
        logger.info("Sent voice note: %s", audio_path)


def send(audio_path: str):
    # Backward-compatible alias.
    send_voice(audio_path)