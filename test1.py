from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Hello, this is a cloned voice!",
    speaker_wav="sample.wav",   # your reference audio
    language="en",
    file_path="output.wav"
)