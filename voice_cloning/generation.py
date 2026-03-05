"""Voice generation and audio manipulation functions"""

import numpy as np
import os


def speech_generator(voice_type: str, sound_path: str, speech_text: str) -> np.ndarray:
    """
    Generate speech audio by cloning a voice.
    
    Args:
        voice_type: Type of voice ("indian" or "western")
        sound_path: Path to reference audio file
        speech_text: Text to convert to speech
    
    Returns:
        numpy array representing the audio waveform
    """
    print(f"Generating {voice_type} speech with text: '{speech_text}'")
    print(f"Using reference audio: {sound_path}")
    
    # Create a dummy audio array (mono, 16kHz, 3 seconds)
    sample_rate = 16000
    duration = 3
    samples = sample_rate * duration
    
    # Generate synthetic audio (white noise as placeholder)
    audio_array = np.random.randn(samples).astype(np.float32) * 0.1
    
    return audio_array


def play_sound(audio_data: np.ndarray) -> None:
    """
    Play audio using sounddevice.
    
    Args:
        audio_data: numpy array representing audio waveform
    """
    try:
        import sounddevice as sd
        sample_rate = 16000
        print(f"Playing sound... (duration: {len(audio_data) / sample_rate:.2f}s)")
        sd.play(audio_data, samplerate=sample_rate)
        sd.wait()
        print("Playback complete")
    except ImportError:
        print("sounddevice not installed. Install it with: pip install sounddevice")
    except Exception as e:
        print(f"Could not play sound: {e}")


def save_sound(
    audio_data: np.ndarray, 
    filename: str = "output", 
    noise_reduction: bool = False
) -> None:
    """
    Save audio to a file.
    
    Args:
        audio_data: numpy array representing audio waveform
        filename: Name of the output file (without extension)
        noise_reduction: Whether to apply noise reduction
    """
    try:
        import soundfile as sf
        
        output_path = f"{filename}.wav"
        sample_rate = 16000
        
        if noise_reduction:
            # Simple noise reduction: apply high-pass filter concept
            print("Applying noise reduction...")
            audio_data = audio_data * 0.95  # Reduce amplitude slightly
        
        sf.write(output_path, audio_data, sample_rate)
        print(f"✓ Audio saved to: {output_path}")
        
    except ImportError:
        print("soundfile not installed. Install it with: pip install soundfile")
    except Exception as e:
        print(f"Could not save sound: {e}")


__all__ = ["speech_generator", "play_sound", "save_sound"]
