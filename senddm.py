from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv
from telethon.tl.types import InputPeerUser
import asyncio
load_dotenv()
api_id=os.getenv("API_ID")
api_hash=os.getenv("API_HASH")
phone = '+919339759265'  

client = TelegramClient('session', api_id, api_hash)
client.connect()
chat_id=TelegramClient.get_entity('me')  # Replace with the username or user ID of the recipient
async def send_audio(audio_path:str ):
    async with client:
        await client.send_file(
            chat_id,
            audio_path,
            voice_note=True,
            caption="🌸 আজকের বার্তা"
        )
        print(f"✅ Sent: {audio_path}")

def send_audio_sync(audio_path:str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_audio(audio_path))

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter OTP: '))

try:
    me = client.get_entity('me')  # Replace with the username or user ID of the recipient
    client.send_message(me, "Hello from Python!", parse_mode='html')
    client.send_file(me, 'my_audio.mp3', caption="Here's an audio file for you!")
    print("Message sent!")
except Exception as e:
    print("Error:", e)

client.disconnect()