from midiutils.types import NoteEvent
from mido.midifiles import MidiFile


class NoteAnimationModel:
  def __init__(
    self,
    bpm: int,
    fps: int,
    ticks_per_beat: int,
    screen_height: int,
    note_speed: int,
  ):
    self.bpm = bpm
    self.fps = fps
    self.ticks_per_beat = ticks_per_beat
    self.screen_height = screen_height
    self.note_speed = note_speed

    # Derived constants
    self.ticks_per_second = self._calculate_ticks_per_second()
    self.frames_per_tick = self._calculate_frames_per_tick()
    self.pixels_per_frame = self._calculate_pixels_per_frame()
    self.ticks_per_frame = self._calculate_ticks_per_frame()

  def _calculate_ticks_per_second(self) -> float:
    """Calculate how many ticks occur in one second.

    The calculation is based on BPM and ticks per beat.
    """
    beats_per_second = self.bpm / 60  # Convert BPM to BPS(Beats Per Second)
    return beats_per_second * self.ticks_per_beat

  def _calculate_frames_per_tick(self) -> float:
    """Calculate the number of frames that occur for each tick."""
    return 1 / (self.ticks_per_second / self.fps)

  def _calculate_pixels_per_frame(self):
    """Calculate how many pixels a note moves in each frame."""
    return self.note_speed / self.fps

  def _calculate_ticks_per_frame(self):
    return self.ticks_per_second / self.fps

  def get_total_number_of_frames(self, events: list[NoteEvent]):
    """Calculate the total number of frames needed to render all notes."""
    # Find the last note event
    last_event = max(events, key=lambda x: x.end)
    # Calculate the total number of ticks needed to render all notes
    total_ticks = last_event.end
    # Calculate the total number of frames needed to render all notes
    return int(total_ticks / self.ticks_per_frame) + 3 * self.fps

  def get_note_position(
    self, start_tick: int, current_frame: int, piano_height: int = 185
  ):
    """Calculate the position of a note in pixels from the top of the screen 0.
    The position is the bottom of the note, relative to the top of the screen.
    """
    # speed affects the number of pixels a note moves in each frame
    ticks_elapsed = current_frame * self.ticks_per_frame
    ticks_relative_frame = start_tick - ticks_elapsed
    seconds_relative_frame = (
      ticks_relative_frame / self.ticks_per_second
    )  # calculate the hight of the note relative to a frame
    pixels_relative_frame = seconds_relative_frame * self.note_speed
    # the return value is the position where the top left is 0 0.

    note_hight_relavtive_to_bottom = (
      self.screen_height - pixels_relative_frame - piano_height
    )
    return note_hight_relavtive_to_bottom

  def _binary_search(self, note_events: list[NoteEvent], start_tick: float):
    """Find the index of the first note that has not passed the piano."""
    left, right = 0, len(note_events) - 1
    while left <= right:
      mid = left + (right - left) // 2
      if note_events[mid].end < start_tick:
        left = mid + 1
      else:
        right = mid - 1
    return left

  def get_active_note_events(
    self,
    note_events: list[NoteEvent],
    current_frame: int,
    screen_height: int,
    piano_height: int,
  ):
    """Return a list of active notes based on the current frame.

    Active notes are notes that are currently present on the frame.
    Dependent variables:
    - note_events: List of NoteEvent objects, each has a start and end tick.
    - current_frame: The current frame being rendered.
    - screen_height: The height of the screen in pixels.
    - speed: The speed of the notes in pixels per second.
    """
    active_notes: list[NoteEvent] = []
    ticks_elapsed = current_frame * self.ticks_per_frame

    # how many seconds does it take for a note to reach the bottom of the screen
    # how many ticks does it take for a note to reach the bottom of the screen
    # note_speed = pixels per second
    seconds_to_reach_piano_from_top = (
      screen_height - piano_height
    ) / self.note_speed
    ticks_to_reach_piano_from_top = (
      seconds_to_reach_piano_from_top * self.ticks_per_second
    )

    end_ticks = ticks_elapsed + ticks_to_reach_piano_from_top

    # We start from the assumption that notes are sorted by their start tick.
    # find the index of the first note that has not started yet with binary
    # search
    start_index = self._binary_search(note_events, ticks_elapsed - 2000)

    for note in note_events[start_index:]:
      # If the note has not started yet, skip it
      if note.start > end_ticks:
        break
      else:
        active_notes.append(note)
    return active_notes

  def get_total_ticks(self, midi_file: MidiFile):
    return midi_file.ticks_per_beat * (self.bpm / 60) * midi_file.length

  def get_note_length(self, duration: int):
    """Calculate the length of a note in pixels based on its duration in ticks."""
    # Convert duration from ticks to seconds
    # Duration in seconds = (Duration in ticks) / (Ticks per second)
    duration_in_seconds = duration / self.ticks_per_second

    # Convert duration from seconds to pixels
    # Length in pixels = Duration in seconds * Note speed (pixels per second)
    length_in_pixels = duration_in_seconds * self.note_speed

    return length_in_pixels
