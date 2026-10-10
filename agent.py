import os
import asyncio
from dotenv import load_dotenv
from backboard import BackboardClient

from tabpfn_tool import FatigueClassifier
from serp_tool import OutdoorScout
from elevenlabs_tool import VoiceAgent

load_dotenv()

class TouchGrassAgent:
    def __init__(self):
        self.fatigue_model = FatigueClassifier()
        self.scout = OutdoorScout()
        self.voice = VoiceAgent()
        
        api_key = os.getenv("BACKBOARD_API_KEY", "")
        if api_key and api_key != "your_backboard_key_here":
            self.client = BackboardClient(api_key=api_key)
        else:
            self.client = None
            
        self.developer_thread_id = "dev_yash_session_001"

    async def evaluate_and_intervene(self, telemetry_data: dict) -> dict:
        burnout_prob = self.fatigue_model.predict_burnout(telemetry_data)

        if burnout_prob < 0.75:
            return {
                "intervention_required": False,
                "burnout_probability": burnout_prob,
                "message": "Flow state active. Keep coding."
            }

        places = self.scout.find_nearby_green_spaces("Indore")
        weather = self.scout.get_weather_conditions("Indore")
        target_park = places[0]['name']
        
        system_prompt = (
            "You are the 'Touch Grass' anti-burnout agent. Your job is to aggressively "
            "but humorously tell the developer to stop coding, lock their screen, and go outside. "
            "Be witty, use gaming/coding metaphors, and keep it strictly under 3 sentences."
        )
        
        user_prompt = (
            f"Developer burnout probability is at {burnout_prob * 100:.2f}%. "
            f"The weather outside is {weather}. Tell them to go to {target_park} right now."
        )

        fallback_message = (
            f"SYSTEM OVERRIDE: Warning! {burnout_prob * 100:.0f}% fatigue reached. "
            f"Drop the keyboard and march to {target_park}. "
            f"It is {weather} outside, you have no excuse. Go touch grass!"
        )

        if self.client:
            try:
                # Pass user_prompt as a direct positional argument, removing 'message='
                response = await self.client.send_message(
                    user_prompt,
                    system=system_prompt,
                    model="google/gemma-2-9b-it",
                    thread_id=self.developer_thread_id
                )
                agent_message = response.content
            except Exception as e:
                print(f"[Backboard Error Triggered]: {e}")
                agent_message = fallback_message
        else:
            agent_message = fallback_message

        # Generate the audio file from the agent's message
        audio_file = self.voice.generate_audio(agent_message)

        return {
            "intervention_required": True,
            "burnout_probability": burnout_prob,
            "target_location": target_park,
            "weather": weather,
            "agent_directive": agent_message,
            "audio_file_generated": bool(audio_file)
        }