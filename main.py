import os
from sarvamai import SarvamAI
from dotenv import load_dotenv
import base64
# Load variables from .env file
load_dotenv()

# Initialize the client using os.getenv()
client = SarvamAI(
    api_subscription_key=os.getenv("YOUR_API_SUBSCRIPTION_KEY"),
)
# Text to convert to speech

response = client.text_to_speech.convert(
    text="नमस्ते, आप कैसे हैं?",
    target_language_code="hi-IN",
    speaker="shubh",
    model="bulbul:v3"
)

# The response object contains a list of base64 strings in the 'audios' attribute
audio_base64 = response.audios[0] 

# Decode and save to file
with open("output.wav", "wb") as f:
    f.write(base64.b64decode(audio_base64))

