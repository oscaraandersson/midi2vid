import json
import os
import unittest

from midi2vid.piano import Note, Piano

config_path = os.path.join(os.path.dirname(__file__), "resources/default.json")

with open(config_path, "r") as f:
  config = json.load(f)


class TestPiano(unittest.TestCase):
  def test_get_left_key_pos_start(self):
    # test for left most key that is an a
    note = Note(key="a", octave=0)
    left = Piano().get_left_key_pos(
      note=note, white_key_width=100, black_key_width=60
    )
    assert left == 0

  def test_get_note(self):
    # test for middle c with note number 60
    note = Piano().get_note(midi_note_number=60)
    assert note.key == "c"
    assert note.octave == 4
