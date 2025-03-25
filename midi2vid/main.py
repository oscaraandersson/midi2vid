"""Entrypoint to run generate a video from a midi file."""

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

from midi2hands.models.generative import GenerativeHandFormer
from midi2hands.models.onnex.onnex_model import ONNXModel
from midiutils.midi_preprocessor import MidiPreprocessor

from midi2vid.config import Config
from midi2vid.download_soundfont import download_soundfont
from midi2vid.video_generator import VideoGenerator


def main(source_path: Path, video_path: Path, config: Config):
  """Entry point of the program."""
  # check if the sound font is downloaded
  download_soundfont()

  with TemporaryDirectory() as workdir:
    preprocessor = MidiPreprocessor()
    video_generator = VideoGenerator(workdir=Path(workdir), midi_file_path=source_path, config=config)

    events = []
    events = preprocessor.get_midi_events(source_path, max_note_length=int(config.max_note_length))
    if config.estimate_hands:
      model = ONNXModel()
      handformer = GenerativeHandFormer(model=model)
      _, _, y_pred = handformer.inference(events=events, window_size=model.window_size, device="cpu")
      for i, e in enumerate(events):
        e.hand = "left" if y_pred[i] == 0 else "right"
    video_generator.generate_video(events=events, destination_filepath=video_path)


def parse_color(color_str):
  """Convert comma-separated RGB string to list of ints."""
  return [int(x.strip()) for x in color_str.split(",")]


def get_parser():
  parser = argparse.ArgumentParser(description="Configuration for note display")

  # Integer arguments
  parser.add_argument("input", type=str, nargs="?", default=None, help="Input MIDI file path")
  parser.add_argument("output", type=str, nargs="?", default=None, help="Output video file path")

  parser.add_argument("-i", "--input", type=str, dest="input_opt", help="Input MIDI file path (overrides positional)")
  parser.add_argument("-o", "--output", type=str, dest="output_opt", help="Output video file path (overrides positional)")

  parser.add_argument("--max-note-length", type=int, default=80, help="Maximum length of notes")
  parser.add_argument("--n-processors", type=int, default=4, help="Number of processors to use")
  parser.add_argument("--screen-width", type=int, default=1920, help="Screen width in pixels")
  parser.add_argument("--screen-height", type=int, default=1080, help="Screen height in pixels")
  parser.add_argument("--fps", type=int, default=30, help="Frames per second")
  parser.add_argument("--speed", type=int, default=300, help="Note falling speed")
  parser.add_argument("--estimate-hands", action="store_true", default=True, help="Enable hand estimation")
  parser.add_argument("--no-estimate-hands", action="store_false", dest="estimate_hands", help="Disable hand estimation")
  parser.add_argument("--debug", action="store_true", default=False, help="Enable debug mode")

  # Color arguments (RGB triplets)
  parser.add_argument("--white-note-color", type=parse_color, default="255,255,255", help="White note color as RGB (comma-separated)")
  parser.add_argument("--black-note-color", type=parse_color, default="49,49,49", help="Black note color as RGB (comma-separated)")
  parser.add_argument("--background-color", type=parse_color, default="43,43,43", help="Background color as RGB (comma-separated)")
  parser.add_argument("--octave-lines-color", type=parse_color, default="92,92,92", help="Octave lines color as RGB (comma-separated)")
  parser.add_argument("--note-color", type=parse_color, default="179,44,49", help="Note color as RGB (comma-separated)")
  parser.add_argument("--dark-note-color", type=parse_color, default="113,34,36", help="Dark note color as RGB (comma-separated)")
  parser.add_argument("--right-note-color", type=parse_color, default="168,255,145", help="Right hand note color as RGB (comma-separated)")
  parser.add_argument("--left-note-color", type=parse_color, default="176,202,229", help="Left hand note color as RGB (comma-separated)")
  parser.add_argument("--dark-right-note-color", type=parse_color, default="118,208,68", help="Dark right hand note color as RGB (comma-separated)")
  parser.add_argument("--dark-left-note-color", type=parse_color, default="124,142,151", help="Dark left hand note color as RGB (comma-separated)")

  return parser


def commandline_main():
  """Parse the arguments and call main."""
  parser = get_parser()
  args = parser.parse_args()
  # Filter out input/output args and create config with remaining args
  config_args = {k: v for k, v in vars(args).items() if k not in {"input", "output", "input_opt", "output_opt"}}
  config = Config(**config_args)

  parser = argparse.ArgumentParser(description="Convert midi to mp4")

  # Determine final input and output values
  input_file = args.input_opt if args.input_opt is not None else args.input
  output_file = args.output_opt if args.output_opt is not None else args.output

  # Handle missing arguments with sensible defaults or errors
  if input_file is None:
    raise ValueError("No input file specified. Please provide an input MIDI file.")
  if output_file is None:
    # Derive output from input if possible, or use a default
    if input_file is not None:
      output_file = input_file.split(".")[0] + ".mp4"
    else:
      raise ValueError("No output file specified and no input to derive from.")

  output_file = Path(output_file)
  input_file = Path(input_file)

  assert input_file.exists(), f"Input file {input_file} does not exist"

  main(Path(input_file), Path(output_file), config)


if __name__ == "__main__":
  commandline_main()
