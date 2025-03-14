"""Generates a video of notes from a midi file."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import time
from functools import wraps
from multiprocessing import Pool
from pathlib import Path
from typing import Any, Callable, Dict, TypeVar

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from midiutils.types import NoteEvent
from mido import MidiFile  # type: ignore
from pygame import Surface

from midi2vid.config import Config
from midi2vid.note_animation import NoteAnimationModel
from midi2vid.piano import Note, Piano

# Set up logging configuration
logging.basicConfig(
  level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

T = TypeVar("T")


def log_performance(func: Callable[..., T]) -> Callable[..., T]:
  """Loggs the execution time of a function or method.

  Example usage:
    @log_performance
    def calculation():
  """

  @wraps(func)
  def wrapper(*args: Any, **kwargs: Any) -> T:
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    logging.info(f"{func.__name__} took {execution_time:.4f} ms")
    return result

  return wrapper


def _run_command(command: str, debug: bool = False):
  """Helper function to run shell commands with optional debugging."""
  if debug:
    print(f"Running command: {command}")

  result = subprocess.run(command, shell=True, capture_output=True, text=True)

  if result.returncode != 0:
    print(f"Error executing command:\n{result.stderr}")
    raise RuntimeError(f"Command failed: {command}")

  if debug:
    print(f"Output:\n{result.stdout}")


class VideoGenerator:
  """Generates a video from a midi file of the piano notes."""

  def __init__(self, workdir: Path, midi_file_path: Path, config: Config):
    """Will raise an error if the midi_file_path does not exist."""
    self.workdir = workdir
    self.framedir = self.workdir / "frames"
    self.framedir.mkdir()

    self.config = config
    self.midi_file_path = midi_file_path
    self.piano = Piano(
      screen_width=config.screen_width, screen_height=config.screen_height
    )
    self.note_animation_model = NoteAnimationModel(
      bpm=config.bpm,
      fps=config.fps,
      ticks_per_beat=MidiFile(self.midi_file_path).ticks_per_beat,
      screen_height=config.screen_height,
      note_speed=config.speed,
    )
    self.active_notes: Dict[int, None | NoteEvent] = {
      i: None for i in self.piano.midi_key_range
    }
    self.soundfont_path = os.path.join(
      os.path.dirname(__file__), "data/soundfont.sf2"
    )

  def _render_frames(self):
    command = (
      f"ffmpeg -framerate {self.config.fps} -i {self.framedir}/%5d.jpg "
      f"-c:v libx264 -r {self.config.fps} "
      f"{self.framedir}/video-no-sound.mp4"
    )
    _run_command(command, self.config.debug)

  def _render_audio(self):
    command = (
      f"fluidsynth -ni {self.soundfont_path} {self.midi_file_path} "
      f"-F {self.workdir}/audio.wav"
    )
    _run_command(command, self.config.debug)

  def _merge_audio_and_video(self, destination_filepath: Path):
    command = (
      f"ffmpeg -y -i {self.framedir}/video-no-sound.mp4 "
      f"-i {self.workdir}/audio.wav -c:v copy "
      f"-c:a aac -strict experimental -b:a 192k -f mp4 "
      f"{destination_filepath.absolute()}"
    )
    _run_command(command, self.config.debug)

  def _draw_vertical_lines(self, screen: Surface, screen_height: int):
    left_positions: list[int] = []
    for midi_note_number in self.piano.midi_key_range:
      note = self.piano.get_note(midi_note_number)
      if "c" in note.key or "f" in note.key:
        left = self.piano.get_left_key_pos(
          note, self.piano.white_key_width, self.piano.black_key_width
        )
        left_positions.append(left)
    for left_pos in left_positions:
      s = pygame.Surface((1, int(screen_height)))
      s.set_alpha(50)
      s.fill((255, 255, 255))
      screen.blit(s, (left_pos, 0))

  def _draw_piano(self, screen: Surface):
    white_key_width = self.piano.white_key_width
    black_key_width = self.piano.black_key_width
    white_key_height = self.piano.white_key_height
    black_key_height = white_key_height - 0.4 * white_key_height
    top = self.config.screen_height - white_key_height

    self._draw_vertical_lines(screen, self.config.screen_height)

    # Draw white keys
    for midi_note_id in self.piano.midi_key_range:
      note: Note = self.piano.get_note(midi_note_id)
      if "#" in note.key:
        continue
      left_pos = self.piano.get_left_key_pos(
        note, white_key_width, black_key_width
      )
      color = self.config.white_note_color
      note_event = self.active_notes[midi_note_id]
      if note_event:
        if note_event.hand == "right":
          color = self.config.right_note_color
        elif note_event.hand == "left":
          color = self.config.left_note_color
        else:
          # if hand is not set, it means it's a note that is played by both
          # hands
          color = self.config.note_color
      rect = pygame.Rect(left_pos, top, white_key_width, white_key_height)
      pygame.draw.rect(screen, color, rect, border_radius=3)
      pygame.draw.rect(screen, (0, 0, 0), rect, 1, border_radius=3)

    # Darw black keys
    for midi_note_id in self.piano.midi_key_range:
      note: Note = self.piano.get_note(midi_note_id)
      if "#" not in note.key:
        continue
      color = self.config.black_note_color
      note_event = self.active_notes[midi_note_id]
      if note_event:
        if note_event.hand == "right":
          color = self.config.dark_right_note_color
        elif note_event.hand == "left":
          color = self.config.dark_left_note_color
        else:
          color = self.config.dark_note_color

      left = self.piano.get_left_key_pos(note, white_key_width, black_key_width)
      rect = pygame.Rect(left, top, black_key_width, black_key_height)
      pygame.draw.rect(screen, color, rect, border_radius=3)

  def _save_frame(self, path: Path, screen: Surface, frame_number: int):
    pygame.image.save(screen, f"{path}/{frame_number:05}.jpg")

  def _is_active(self, note_position: int, duration: float, midi_note_id: int):
    white_key_height_relative_bottom = (
      self.config.screen_height - self.piano.white_key_height
    )
    if (
      note_position > white_key_height_relative_bottom
      and (note_position - duration) < white_key_height_relative_bottom
    ):
      return True

  def _draw_note(
    self, note_event: NoteEvent, frame_id: int, screen: pygame.Surface
  ):
    note_padding = 2
    note: Note = self.piano.get_note(note_event.note)
    white_key_width = self.piano.white_key_width
    black_key_width = self.piano.black_key_width

    if "#" in note.key:
      width = self.piano.black_key_width
      if note_event.hand == "right":
        color = self.config.dark_right_note_color
      elif note_event.hand == "left":
        color = self.config.dark_left_note_color
      else:
        color = self.config.dark_note_color
      note_padding = 0
    else:
      width = self.piano.white_key_width - note_padding * 2
      if note_event.hand == "right":
        color = self.config.right_note_color
      elif note_event.hand == "left":
        color = self.config.left_note_color
      else:
        color = self.config.note_color

    # logging.info(f"note {note} is active")
    note_position = round(
      self.note_animation_model.get_note_position(
        start_tick=note_event.start,
        current_frame=frame_id,
        piano_height=int(self.piano.white_key_height),
      )
    )  # the top of the note relative to the top of the screen which is 0

    left_pos = (
      self.piano.get_left_key_pos(note, white_key_width, black_key_width)
      + note_padding
    )
    # darw the note
    duration = self.note_animation_model.get_note_length(
      note_event.end - note_event.start
    )
    note_top = note_position - duration
    white_key_height_relative_bottom = (
      self.config.screen_height - self.piano.white_key_height
    )
    if self._is_active(note_position, duration, note_event.note):
      self.active_notes[note_event.note] = note_event
    # self._set_active_notes(note_position, duration, note_event.note)
    if note_top < white_key_height_relative_bottom:
      pygame.draw.rect(
        screen,
        color,
        pygame.Rect(left_pos, note_top, width, duration),
        border_radius=3,
      )

  def _generate_frame(
    self, events: list[NoteEvent], frame_id: int, screen: Surface
  ) -> None:
    # reset active notes
    self.active_notes = {note: None for note in self.piano.midi_key_range}
    screen.fill(self.config.background_color)
    # select the events that are in the current frame
    active_events: list[NoteEvent] = (
      self.note_animation_model.get_active_note_events(
        note_events=events,
        current_frame=frame_id,
        screen_height=self.config.screen_height,
        piano_height=int(self.piano.white_key_height),
      )
    )
    # draw the notes that are in the current frame
    for (
      note_event
    ) in active_events:  # draw all the notes that will hit a white key
      if "#" not in self.piano.get_note(note_event.note).key:
        self._draw_note(note_event, frame_id, screen)
    for (
      note_event
    ) in active_events:  # draw all the notes that will hit a black key
      if "#" in self.piano.get_note(note_event.note).key:
        self._draw_note(note_event, frame_id, screen)
    self._draw_piano(screen)
    self._save_frame(path=self.framedir, screen=screen, frame_number=frame_id)

  def _generate_frame_range(
    self, events: list[NoteEvent], start_frame: int, end_frame: int
  ):
    screen = pygame.Surface(
      (self.config.screen_width, self.config.screen_height)
    )
    for frame_id in range(start_frame, end_frame):
      self._generate_frame(events, frame_id, screen)

  def _generate_frames(self, events: list[NoteEvent]):
    total_frames = self.note_animation_model.get_total_number_of_frames(events)
    logging.info(f"Total frames: {total_frames}")
    n_processors = self.config.n_processors
    frames_per_process = total_frames // n_processors
    with Pool(n_processors) as p:
      p.starmap(
        self._generate_frame_range,
        [
          (events, i * frames_per_process, (i + 1) * frames_per_process)
          for i in range(n_processors)
        ],
      )

  @log_performance
  def generate_video(
    self,
    events: list[NoteEvent],
    destination_filepath: Path,
  ):
    """Generate a video of a midi file path.

    The events could be generated with the midi_preprocessor.
    """
    logging.info("Generating frames")
    self._generate_frames(events)
    logging.info("Rendering video")
    self._render_frames()
    logging.info("Rendering audio")
    self._render_audio()
    logging.info("Merging audio and video")
    self._merge_audio_and_video(destination_filepath)

    if self.config.debug:
      shutil.copytree(self.workdir, "workdir", dirs_exist_ok=True)
