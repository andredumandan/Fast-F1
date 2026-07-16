# fastf1-service/main.py
import asyncio
from typing import List, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastf1 import SignalRClient

app = FastAPI(title="FastF1 Live API")

# Allow CORS from any origin (for dev purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In‑memory store of the latest telemetry per driver
latest_telemetry: Dict[int, dict] = {}

async def signalr_worker() -> None:
    """Connect to the official F1 feed and update *latest_telemetry*.
    This runs in a background task started when the FastAPI app starts."""
    client = SignalRClient()
    await client.start_async()

    async for msg in client.messages:
        # Each message is a dict containing telemetry data.  We store it keyed by driver number.
        if isinstance(msg, dict) and "driverNumber" in msg:
            driver_number = int(msg["driverNumber"])
            latest_telemetry[driver_number] = msg

    await client.stop_async()

# Start the SignalR worker when the app starts up
@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(signalr_worker())

class TelemetryResponse(BaseModel):
    driverNumber: int
    lapNumber: int | None = None
    gapToLeader: float | None = None
    speedKmh: float | None = None
    isPitStopped: bool | None = None

@app.get("/live", response_model=List[TelemetryResponse])
async def get_live() -> List[TelemetryResponse]:
    if not latest_telemetry:
        raise HTTPException(status_code=503, detail="No telemetry available yet")
    # Convert internal dicts to TelemetryResponse objects
    return [TelemetryResponse(**{k: v for k, v in d.items() if k in TelemetryResponse.__fields__})
            for d in latest_telemetry.values()]
