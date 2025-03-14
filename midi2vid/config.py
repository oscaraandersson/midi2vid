import json
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Config:
  max_note_length: int
  n_processors: int
  screen_width: int
  screen_height: int
  bpm: int
  fps: int
  speed: int
  white_note_color: List[int]
  black_note_color: List[int]
  background_color: List[int]
  octave_lines_color: List[int]
  note_color: List[int]
  dark_note_color: List[int]
  right_note_color: List[int]
  left_note_color: List[int]
  dark_right_note_color: List[int]
  dark_left_note_color: List[int]
  estimate_hands: bool
  debug: bool

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
