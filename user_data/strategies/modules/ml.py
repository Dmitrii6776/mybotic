# user_data/modules/ml.py

import logging
import os

logger = logging.getLogger(__name__)

# Optional placeholder for FreqAI integration
FREQAI_ENABLED = True  # Set False if using external model

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'price_predictor.pkl')

def load_model():
    """
    Loads a pre-trained ML model (if using pickle approach).
    With FreqAI, this would instead return FreqAI context object or config reference.
    """
    if FREQAI_ENABLED:
        logger.info("FreqAI integration mode: external model loading skipped (handled by FreqAI).")
        return None  # FreqAI manages its own model pipeline
    try:
        import pickle
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        logger.info("ML model loaded successfully (external pickle).")
        return model
    except Exception as e:
        logger.error(f"Error loading ML model: {e}")
        return None

def predict_price_movement(symbol: str, features: list) -> int:
    """
    Predicts price movement.
    With FreqAI, this would be a call to FreqAI's prediction output inside populate_indicators().
    """
    if FREQAI_ENABLED:
        logger.info(f"FreqAI integration active: prediction for {symbol} delegated to FreqAI pipeline.")
        # FreqAI predictions are injected into dataframe automatically via feature pipelines
        return 0  # Placeholder; actual score should be read from dataframe['freqai_prediction']
    
    model = load_model()
    if not model:
        logger.warning("Prediction skipped: no model loaded (external mode).")
        return 0
    try:
        prediction = model.predict([features])[0]
        logger.info(f"Predicted movement for {symbol}: {prediction}")
        return prediction
    except Exception as e:
        logger.error(f"Prediction error for {symbol}: {e}")
        return 0