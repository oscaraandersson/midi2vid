class Note:
  def __init__(self, key: str, octave: int):
    self.key = key
    self.octave = octave


class Piano:
  def __init__(self, screen_width: int = 1080, screen_height: int = 720):
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.midi_number_to_note = self._generate_piano_midi_representation()
    self.n_white_keys = 52
    self.midi_key_range = range(21, 108 + 1)

    self.white_key_width = self.screen_width / self.n_white_keys
    self.white_key_height = 5 * self.white_key_width
    self.black_key_width = self.white_key_width * 0.6

  def _generate_piano_midi_representation(self) -> dict[int, Note]:
    note_names = [
      "c",
      "c#",
      "d",
      "d#",
      "e",
      "f",
      "f#",
      "g",
      "g#",
      "a",
      "a#",
      "b",
    ]
    start_note = "a"
    note_index = note_names.index(start_note)
    octave = 0
    piano: dict[int, Note] = {}
    for midi_note_number in range(21, 108 + 1):
      piano[midi_note_number] = Note(
        key=f"{note_names[note_index % len(note_names)]}", octave=octave
      )
      note_index += 1
      if note_index % len(note_names) == 0:
        octave += 1
    return piano

  def get_left_key_pos(
    self, note: Note, white_key_width: float, black_key_width: float
  ) -> int:
    start_key = "a"
    octave_distances = {
      "c": 0 * white_key_width,
      "c#": 1 * white_key_width - black_key_width / 2,
      "d": 1 * white_key_width,
      "d#": 2 * white_key_width - black_key_width / 2,
      "e": 2 * white_key_width,
      "f": 3 * white_key_width,
      "f#": 4 * white_key_width - black_key_width / 2,
      "g": 4 * white_key_width,
      "g#": 5 * white_key_width - black_key_width / 2,
      "a": 5 * white_key_width,
      "a#": 6 * white_key_width - black_key_width / 2,
      "b": 6 * white_key_width,
    }

    relative_octave = octave_distances[note.key]
    left = (
      relative_octave
      + (7 * white_key_width * note.octave)
      - octave_distances[start_key]
    )
    return int(left)

  def get_note(self, midi_note_number: int) -> Note:
    return self.midi_number_to_note[midi_note_number]

  def get_key_width(self, note: Note, white_key_width: int) -> float:
    if "#" in note.key:
      return white_key_width * 0.6
    return white_key_width
