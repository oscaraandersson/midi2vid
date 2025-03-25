from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
  max_note_length: int = 80
  n_processors: int = 4
  screen_width: int = 1920
  screen_height: int = 1080
  fps: int = 30
  speed: int = 300
  white_note_color: List[int] = field(default_factory=lambda: [255, 255, 255])
  black_note_color: List[int] = field(default_factory=lambda: [49, 49, 49])
  background_color: List[int] = field(default_factory=lambda: [43, 43, 43])
  octave_lines_color: List[int] = field(default_factory=lambda: [92, 92, 92])
  note_color: List[int] = field(default_factory=lambda: [179, 44, 49])
  dark_note_color: List[int] = field(default_factory=lambda: [113, 34, 36])
  right_note_color: List[int] = field(default_factory=lambda: [168, 255, 145])
  left_note_color: List[int] = field(default_factory=lambda: [176, 202, 229])
  dark_right_note_color: List[int] = field(default_factory=lambda: [118, 208, 68])
  dark_left_note_color: List[int] = field(default_factory=lambda: [124, 142, 151])
  estimate_hands: bool = True
  debug: bool = False
