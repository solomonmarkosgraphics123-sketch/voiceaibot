import telebot
from telebot import types
import edge_tts
import asyncio
import os

BOT_TOKEN = "8701594215:AAGwl0xfdecXEXDfYJOd1Q7ydBeCK97XwfU"  # get a fresh one from @BotFather, never reuse a leaked token
bot = telebot.TeleBot(BOT_TOKEN)

# ---------------------------------------------------------
# VOICE LIBRARY
# Structure: LANGUAGES[lang_code] = {
#     "label": "Display name",
#     "male":   {"Voice Actor Name": "edge-tts-voice-id", ...},
#     "female": {"Voice Actor Name": "edge-tts-voice-id", ...}
# }
# All voice IDs below are real, free, official Edge TTS neural voices.
# ---------------------------------------------------------
LANGUAGES = {
    "en": {
        "label": "English (US)",
        "male": {
            "Christopher": "en-US-ChristopherNeural",
            "Guy": "en-US-GuyNeural",
            "Eric": "en-US-EricNeural",
            "Roger": "en-US-RogerNeural",
            "Steffan": "en-US-SteffanNeural",
        },
        "female": {
            "Jenny": "en-US-JennyNeural",
            "Aria": "en-US-AriaNeural",
            "Michelle": "en-US-MichelleNeural",
            "Ana": "en-US-AnaNeural",
            "Emma": "en-US-EmmaNeural",
        },
    },
    "en-gb": {
        "label": "English (UK)",
        "male": {
            "Ryan": "en-GB-RyanNeural",
            "Thomas": "en-GB-ThomasNeural",
        },
        "female": {
            "Sonia": "en-GB-SoniaNeural",
            "Libby": "en-GB-LibbyNeural",
        },
    },
    "am": {
        "label": "Amharic",
        "male": {
            "Ameha": "am-ET-AmehaNeural",
        },
        "female": {
            "Mekdes": "am-ET-MekdesNeural",
        },
    },
    "ar": {
        "label": "Arabic",
        "male": {
            "Hamdan": "ar-SA-HamedNeural",
        },
        "female": {
            "Zariyah": "ar-SA-ZariyahNeural",
        },
    },
}

# per-user selection state: {chat_id: {"lang": "en", "gender": "male", "voice_id": "...", "voice_name": "..."}}
user_state = {}


def get_state(chat_id):
    if chat_id not in user_state:
        user_state[chat_id] = {"lang": "en", "gender": "male", "voice_id": "en-US-ChristopherNeural", "voice_name": "Christopher"}
    return user_state[chat_id]


async def generate_voice(text, voice_id, filename):
    communicate = edge_tts.Communicate(text, voice_id)
    await communicate.save(filename)