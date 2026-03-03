import os
from sarvamai import SarvamAI
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Initialize the client using os.getenv()
client = SarvamAI(
    api_subscription_key=os.getenv("YOUR_API_SUBSCRIPTION_KEY"),
)

response = client.speech_to_text_translate_streaming(
    text="""नमस्ते! Sarvam AI में आपका स्वागत है।

हम भारतीय भाषाओं के लिए अत्याधुनिक voice technology बनाते हैं। हमारे text-to-speech models प्राकृतिक और इंसान जैसी आवाज़ें produce करते हैं, जो बेहद realistic लगती हैं।

आप अपना text type कर सकते हैं या different voices को try करने के लिए किसी भी voice card पर play button पर click कर सकते हैं। तो चलिए, अपनी भाषा में AI की ताकत experience करें!""",
    target_language_code="hi-IN",
    speaker="manan",
    pace=1.1,
    speech_sample_rate=22050,
    enable_preprocessing=True,
    model="bulbul:v3"
)

print(response)