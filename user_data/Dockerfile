FROM freqtradeorg/freqtrade:stable

WORKDIR /freqtrade

# Copy your strategies, configs, user_data
COPY user_data /freqtrade/user_data
COPY config.json /freqtrade/config.json

# OPTIONAL: install extra python deps if needed
# RUN pip install --no-cache-dir -r user_data/requirements.txt

# Expose API port
EXPOSE 8000

# Start both freqtrade & FastAPI under supervisord
CMD ["supervisord", "-c", "/freqtrade/user_data/supervisord.conf"]