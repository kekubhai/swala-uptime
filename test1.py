from elevenlabs_tts import generate_and_save_audio
from senddm import send

audio_path = generate_and_save_audio()
send(audio_path)