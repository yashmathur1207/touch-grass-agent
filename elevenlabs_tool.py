import os
import requests
from dotenv import load_dotenv

load_dotenv()

class VoiceAgent:
    def __init__(self):
        # We tell it to look for the LABEL in the .env file, not the key itself
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.voice_id = "pNInz6obpgDQGcFmaJgB" 

    def generate_audio(self, text: str, output_path: str = "directive.mp3"):
        """Generates spoken audio from text and saves it as an MP3."""
        if not self.api_key or self.api_key == "your_elevenlabs_key_here":
            print("[ElevenLabs] No API key found. Skipping voice generation.")
            return None

        print(f"[ElevenLabs] Synthesizing audio directive...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_turbo_v2", 
            "voice_settings": {
                "stability": 0.5, 
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"[ElevenLabs] Audio saved successfully to {output_path}")
            return output_path
        else:
            print(f"[ElevenLabs Error]: {response.text}")
            return None