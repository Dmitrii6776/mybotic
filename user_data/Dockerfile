FROM continuumio/miniconda3

# Create conda environment
RUN conda create -n myenv python=3.10

# Activate env and install libta-lib
RUN /bin/bash -c "source activate myenv && \
    conda install -c conda-forge libta-lib && \
    pip install ta-lib freqtrade pandas-ta"

# Set working directory
WORKDIR /app

# Copy your app
COPY . .

# Activate env on container start
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Expose port for API (if needed)
EXPOSE 8000

# Run your supervisor (or uvicorn, or freqtrade)
CMD ["supervisord", "-c", "/app/user_data/supervisord.conf"]