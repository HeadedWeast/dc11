FROM python:3.9

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /dc11

# Copy the application code
COPY dc11.py .

ADD dc11.py .

# Install Python dependencies
RUN pip install discord requests PyNaCl
# Add env variables
ENV apikey = "INSERT API KEY FOR ELEVENLABS.IO"
ENV DISCORDBOTKEY = "INSERT DISCORD BOT KEY"
# Expose the port for the Discord bot
EXPOSE 8080

# Start the Discord bot
CMD ["python", "dc11.py"]
