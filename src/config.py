import os
from pathlib import Path


class Config:
    def __init__(self):
        self.SOUND_FONT_PATH = Path(
            os.path.join(os.path.dirname(__file__), "..", "data", "soundfont.sf2")
        )

        # Colors and video configuration
        self.BPM = int(os.getenv("BPM", 120))
        self.FPS = int(os.getenv("FPS", 60))
        self.SPEED = int(os.getenv("SPEED", 200))

        self.WHITE_NOTE_COLOR = self._to_tuple(
            os.getenv("WHITE_NOTE_COLOR", "255,255,255")
        )

        self.BLACK_NOTE_COLOR = self._to_tuple(
            os.getenv("BLACK_NOTE_COLOR", "49,49,49")
        )
        self.BACKGROUND_COLOR = self._to_tuple(
            os.getenv("BACKGROUND_COLOR", "43,42,43")
        )
        self.NOTE_COLOR = self._to_tuple(os.getenv("NOTE_COLOR", "144,213,78"))
        self.DARK_NOTE_COLOR = self._to_tuple(os.getenv("DARK_NOTE_COLOR", "90,140,44"))
        self.OCTAVE_LINES_COLOR = self._to_tuple(
            os.getenv("OCTAVE_LINES_COLOR", "92,92,92")
        )

        self.SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 1080))
        self.SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 1920))

        self.S3_ACCESS_KEY = str(os.getenv("S3_ACCESS_KEY", "minioadmin"))
        self.S3_SECRET_KEY = str(os.getenv("S3_SECRET_KEY", "minioadmin"))
        self.S3_BUCKET_NAME = str(os.getenv("S3_BUCKET_NAME", "files"))
        self.S3_DIR = str(os.getenv("S3_DIR", "files"))

    def _to_tuple(self, color: str):
        return tuple(map(int, color.split(",")))
