FROM python:3.11

# install ffmpeg and fluidsynth
RUN apt-get update && apt-get install -y \
    ffmpeg \
    fluidsynth

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN pip install -e .

CMD ["python3", "src/converter.py"]
