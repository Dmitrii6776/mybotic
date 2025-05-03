from threading import Thread
import time
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json
from user_data import main
from user_data.strategies.modules import (
    custum_data_fetch,
    market_context,
    
)

def fetch_data():
    return custum_data_fetch.fetch_data()

def fetch_metadata():
    return {
        "market_context": market_context.fetch_market_context(),
        "sentiment_data": custum_data_fetch.fetch_sentiment_data(),
        "whale_activity": custum_data_fetch.fetch_whale_activity(),
    }


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json'))
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

app = FastAPI(title="HypeStrategy Data API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'cache')


# --- Background update functions ---
def run_hype_strategy():
    hype = get_strategy("HypeStrategy")
    while True:
        main.run_hype_strategy
        time.sleep(1800)  # refresh every 30 min

def run_scalp_strategy():
    scalp = get_strategy("ScalpingStrategy")
    while True:
        main.run_scalp_strategy
        time.sleep(60)  # refresh every 60 seconds

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


# --- Startup event to launch background threads ---
@app.on_event("startup")
def start_background_tasks():
    logger.info("Starting HypeStrategy and ScalpingStrategy background tasks...")
    Thread(target=run_hype_strategy, daemon=True).start()
    Thread(target=run_scalp_strategy, daemon=True).start()
