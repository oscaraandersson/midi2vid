import json
from pathlib import Path
from typing import List


class Config:
  def __init__(
    self,
    soundfont_path: str,
    max_note_length: int,
    n_processors: int,
    screen_width: int,
    screen_height: int,
    bpm: int,
    fps: int,
    speed: int,
    white_note_color: List[int],
    black_note_color: List[int],
    background_color: List[int],
    octave_lines_color: List[int],
    note_color: List[int],
    dark_note_color: List[int],
    right_note_color: List[int],
    left_note_color: List[int],
    dark_right_note_color: List[int],
    dark_left_note_color: List[int],
  ):
    self.soundfont_path = soundfont_path
    self.max_note_length = max_note_length
    self.n_processors = n_processors
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.bpm = bpm
    self.fps = fps
    self.speed = speed
    self.white_note_color = white_note_color
    self.black_note_color = black_note_color
    self.background_color = background_color
    self.octave_lines_color = octave_lines_color
    self.note_color = note_color
    self.dark_note_color = dark_note_color
    self.right_note_color = right_note_color
    self.left_note_color = left_note_color
    self.dark_right_note_color = dark_right_note_color
    self.dark_left_note_color = dark_left_note_color

  @staticmethod
  def from_json(json_path: Path) -> "Config":
    with open(json_path, "r") as file:
      data = json.load(file)
    return Config(**data)

  def to_dict(self) -> dict[str, list[str] | str | int]:
    return self.__dict__

  def save_to_json(self, json_path: Path) -> None:
    with open(json_path, "w") as file:
      json.dump(self.to_dict(), file, indent=4)
