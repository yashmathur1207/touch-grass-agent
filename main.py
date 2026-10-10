import os
import warnings
import sentry_sdk
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import TouchGrassAgent

# Mute the harmless Pydantic warnings from the Backboard SDK
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

load_dotenv()

# Initialize Sentry
dsn_url = os.getenv("SENTRY_DSN", "")
if dsn_url and dsn_url != "your_sentry_dsn_here":
    sentry_sdk.init(
        dsn=dsn_url,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

app = FastAPI(title="Touch Grass Agent API")
agent = TouchGrassAgent()

# Define the expected incoming data structure
class TelemetryInput(BaseModel):
    session_duration_mins: int
    keystrokes_per_min: int
    error_rate_pct: float
    time_since_last_break_mins: int

@app.get("/")
async def root():
    return {"status": "online", "message": "Ready to touch grass."}

@app.post("/api/evaluate")
async def evaluate_session(telemetry: TelemetryInput):
    # This block wraps the agent in a Sentry trace!
    with sentry_sdk.start_transaction(op="task", name="Evaluate Burnout"):
        
        # Convert the incoming Pydantic data to a standard dictionary
        data = telemetry.model_dump()
        
        # Run the agent
        result = await agent.evaluate_and_intervene(data)
        return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)