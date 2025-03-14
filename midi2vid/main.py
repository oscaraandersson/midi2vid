"""Entrypoint to run generate a video from a midi file."""

import argparse
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from midi2hands.models.generative import GenerativeHandFormer
from midi2hands.models.onnex.onnex_model import ONNXModel
from midiutils.midi_preprocessor import MidiPreprocessor

from midi2vid.config import Config
from midi2vid.download_soundfont import download_soundfont
from midi2vid.video_generator import VideoGenerator


def main(
  config_path: Path,
  source_path: Path,
  video_path: Path,
):
  """Entry point of the program."""
  config = Config.from_json(config_path)

  # check if the sound font is downloaded
  download_soundfont()

  with TemporaryDirectory() as workdir:
    preprocessor = MidiPreprocessor()
    video_generator = VideoGenerator(
      workdir=Path(workdir), midi_file_path=source_path, config=config
    )

    events = []
    events = preprocessor.get_midi_events(
      source_path, max_note_length=int(config.max_note_length)
    )
    if config.estimate_hands:
      model = ONNXModel()
      handformer = GenerativeHandFormer(model=model)
      _, _, y_pred = handformer.inference(
        events=events, window_size=model.window_size, device="cpu"
      )
      for i, e in enumerate(events):
        e.hand = "left" if y_pred[i] == 0 else "right"
    video_generator.generate_video(
      events=events, destination_filepath=video_path
    )


def commandline_main():
  """Parse the arguments and call main."""
  default_config_path = os.path.join(
    os.path.dirname(__file__), "config/default.json"
  )
  parser = argparse.ArgumentParser(description="Convert midi to mp4")
  parser.add_argument("-i", type=str, required=True)
  parser.add_argument("-o", type=str, required=True)
  parser.add_argument(
    "--config", type=str, required=False, default=default_config_path
  )
  args = parser.parse_args()

  source_path = Path(args.i)
  target_path = Path(args.o)
  assert source_path.exists(), f"File {source_path} does not exist"
  assert source_path.is_file(), f"Path {source_path} is not a file"

  config_path = Path(args.config)
  assert config_path.exists(), f"File {config_path} does not exist"
  main(config_path, source_path, target_path)


if __name__ == "__main__":
  commandline_main()
