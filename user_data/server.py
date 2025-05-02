from user_data.strategies.hype_startegy.hype_strategy import HypeStrategy
from user_data.strategies.scalping_strategy.scalping_strategy import ScalpingStrategy
from threading import Thread

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

print("ok")

app = FastAPI(title="HypeStrategy Data API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'cache')

def load_json(filename):
    filepath = os.path.join(CACHE_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load {filename}: {e}")
        return {}

@app.get("/")
def root():
    return {"message": "HypeStrategy Data API running."}

@app.get("/market_context")
def get_market_context():
    return JSONResponse(content=load_json("market_context.json"))

@app.get("/sentiment_data")
def get_sentiment_data():
    return JSONResponse(content=load_json("sentiment_data.json"))

@app.get("/whale_activity")
def get_whale_activity():
    return JSONResponse(content=load_json("whale_activity.json"))

@app.get("/fear_greed")
def get_fear_greed():
    return JSONResponse(content=load_json("fear_greed.json"))


@app.get("/pairlist")
def get_pairlist():
    return JSONResponse(content=load_json("pairlist.json"))

# --- Scalping-specific endpoints ---
@app.get("/scalp_signals")
def get_scalp_signals():
    return JSONResponse(content=load_json("scalp_signals.json"))

# --- Health endpoint ---
@app.get("/health")
def get_health():
    return {"status": "ok", "message": "Server operational."}


# --- Startup event to launch strategies ---
@app.on_event("startup")
def start_strategies():
    logger.info("Starting HypeStrategy and ScalpingStrategy...")
    hype_thread = Thread(target=HypeStrategy.run, daemon=True)
    scalp_thread = Thread(target=ScalpingStrategy.run, daemon=True)
    hype_thread.start()
    scalp_thread.start()


