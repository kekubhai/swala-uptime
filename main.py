import os
from sarvamai import SarvamAI
from dotenv import load_dotenv
import base64
from dailytextgeneration import generate_message, datetime

load_dotenv()


# Initialize the client using os.getenv()
client = SarvamAI(
    api_subscription_key=os.getenv("YOUR_API_SUBSCRIPTION_KEY"),
)
# Text to convert to speech

response = client.text_to_speech.convert(
    text=generate_message(datetime.now().hour, "positive and loving"),
    target_language_code="bn-IN",
    speaker="shubh",
    model="bulbul:v3"
)

# The response object contains a list of base64 strings in the 'audios' attribute
audio_base64 = response.audios[0] 
with open(f"sarvamvoices/output{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3", "wb") as f:
    f.write(base64.b64decode(audio_base64))

