from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os
import datetime

load_dotenv()

elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


def text_to_voice(text: str) -> str:
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="ViGox7moQtO0AJtyWAqT",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    output_dir = "elevenlabsvoices"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/output{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"

    with open(filename, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return filename

def generate_and_save_audio() -> str:
    from dailytextgeneration import generate_message

    text = generate_message()
    return text_to_voice(text)