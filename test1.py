from voice_cloning.generation import *
import librosa
import soundfile as sf
import numpy as np

# ── Step 1: Convert & clean your MP3 → WAV ──────────────────────────
raw_audio, sr = librosa.load("my_audio.mp3", sr=22050, mono=True)

# Normalize to prevent clipping/distortion
raw_audio = raw_audio / (np.max(np.abs(raw_audio)) + 1e-9)

# Save clean WAV
sf.write("my_audio_clean.wav", raw_audio, 22050)
print(f"Audio loaded: {len(raw_audio)/22050:.1f} seconds at {sr}Hz")

# ── Step 2: Clone ────────────────────────────────────────────────────
speech_text = "Please use this package carefully"

generated_wav = speech_generator(
    voice_type = "indian",
    sound_path = "my_audio_clean.wav",  # use cleaned WAV, not original MP3
    speech_text = speech_text,
)

# ── Step 3: Save & play ──────────────────────────────────────────────
play_sound(generated_wav)
save_sound(generated_wav, filename="voice_output", noise_reduction=True)