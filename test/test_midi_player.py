import json
import os
import time
import unittest
from pathlib import Path

from src.video_generator.piano import Note, Piano
from src.video_generator.video_generator import VideoGenerator

config_path = os.path.join(os.path.dirname(__file__), "resources/default.json")

with open(config_path, "r") as f:
  config = json.load(f)


class TestVideoGenerator(unittest.TestCase):
  def setUp(self):
    # setup workdir
    current_time = str(time.time()).replace(".", "-")
    self.workdir = Path(
      f"{Path(__file__).parent}/resources/workdirs/{current_time}"
    )
    self.workdir.mkdir(parents=True, exist_ok=False)
    midi_file_path = Path(
      f"{Path(__file__).parent}/resources/empty_example_mid.mid"
    )

    self.default_video_generator = VideoGenerator(
      workdir=self.workdir,
      midi_file_path=midi_file_path,
      config=config,
    )

  def tearDown(self):
    # remove workdir
    os.system(f"rm -rf {self.workdir.absolute()}")

  def test_video_generator_raises_exception_if_workdir_does_not_exist(self):
    workdir = Path(f"{Path(__file__).parent}/resources/non_existant_workdir")
    midi_file_path = Path(
      f"{Path(__file__).parent}/resources/empty_example_mid.mid"
    )
    with self.assertRaises(FileNotFoundError) as _:
      _ = VideoGenerator(
        workdir=workdir, midi_file_path=midi_file_path, config=config
      )

  def test_setup_workdir(self):
    # object is created in setup
    workdir = self.workdir
    framedir = workdir / "frames"
    assert framedir.exists()
    # remove workdir


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
