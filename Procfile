# Starts the Flask server using Gunicorn
web: docker run -p $PORT:5001 -e PORT=$PORT -v $PWD:/app <image_id>
# Starts the Freqtrade bot with hype_strategy
worker: python3.10 -m freqtrade trade --config user_data/config.json --strategy hype_strategy