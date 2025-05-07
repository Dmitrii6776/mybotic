# Starts the Flask server using Gunicorn
web: gunicorn server:app --bind 0.0.0.0:$PORT
# Starts the Freqtrade bot with hype_strategy
worker: python3.10 -m freqtrade trade --config user_data/config.json --strategy hype_strategy