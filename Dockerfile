FROM python:3.11

# Install ffmpeg and fluidsynth
RUN apt-get update && apt-get install -y \
    ffmpeg \
    fluidsynth \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -e .


RUN pip install -e .

# Set the default command to use the midi2vid script with input and output arguments
ENTRYPOINT ["midi2vid"]
