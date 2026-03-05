from telethon.sync import TelegramClient
import os
from dotenv import load_dotenv
from telethon.tl.types import InputPeerUser
load_dotenv()
api_id=os.getenv("API_ID")
api_hash=os.getenv("API_HASH")
phone = '+919339759265'  

client = TelegramClient('session', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter OTP: '))

try:
    me = client.get_entity('me')  # Replace with the username or user ID of the recipient
    client.send_message(me, "Hello from Python!", parse_mode='html')
    print("Message sent!")
except Exception as e:
    print("Error:", e)

client.disconnect()