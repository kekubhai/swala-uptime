from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os
import datetime

load_dotenv()
from dailytextgeneration import generate_message

elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def generate_and_save_audio() -> str:
    text = generate_message(datetime.datetime.now().hour, "positive and loving")

    audio = elevenlabs.text_to_speech.convert(
        text=text, 
        voice_id="ViGox7moQtO0AJtyWAqT",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    filename = f"elevenlabsvoices/output{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"

    with open(filename, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return filename  # ← return the path, not the generator