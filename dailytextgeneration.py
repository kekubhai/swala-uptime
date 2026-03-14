import os
import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_time_of_day():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "morning"
    elif hour < 17:
        return "afternoon"
    elif hour < 21:
        return "evening"
    else:
        return "night"

MOOD = "positive and loving"  # You can change this to vary the tone of the message.


def generate_message(time_of_day=None, mood=MOOD):
    if time_of_day is None:
        time_of_day = get_time_of_day()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""You are a caring and loving boyfriend who expresses emotions genuinely and warmly.
Generate a sweet, heartfelt daily check-in message for my girlfriend.

Rules:
- Write the message in Bengali (বাংলা) language
- Keep it short (3-5 lines max)
- Sound natural and human, NOT like an AI wrote it
- Avoid clichés
- Make it feel spontaneous and thoughtful
- Occasionally include a playful or funny line to make her smile
- End with a question to spark a reply

Time of day: {time_of_day}
Mood tone: {mood}

Generate only the message, nothing else.""",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    time_of_day = get_time_of_day()
    print(f"⏰ Time of day: {time_of_day} | 🎭 Mood: {MOOD}\n")

    message = generate_message(time_of_day, MOOD)
    print(f"💬 Generated Message:\n\n{message}")
    