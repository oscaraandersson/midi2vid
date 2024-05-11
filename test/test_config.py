from src.config import Config
import os


def test_config_to_tuple():
    config = Config()
    color = "255,255,255"
    assert config._to_tuple(color) == (255, 255, 255)


def test_config_soundfont():
    config = Config()
    assert os.path.exists(config.SOUND_FONT_PATH)
