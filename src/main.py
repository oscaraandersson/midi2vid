import os
import argparse
from src.video_generator.midi_preprocessor import MidiPreprocessor
from pathlib import Path
import os
from src.video_generator.video_generator import VideoGeneratorConfig
from src.video_generator.video_generator import VideoGenerator
from src.config import Config


config = Config()


def convert_video(midi_file_path: str, target_video_path: str):
    midi_path = Path(midi_file_path)
    video_path = Path(target_video_path)
    workdir = Path("workdir")
    if workdir.exists():
        os.system("rm -rf workdir")
    workdir.mkdir(parents=True, exist_ok=False)

    preprocessor = MidiPreprocessor()

    video_config = VideoGeneratorConfig(
        bpm=config.BPM,
        fps=config.FPS,
        speed=config.SPEED,
        ticks_per_beat=preprocessor.get_ticks_per_beat(midi_path),
        white_note_color=config.WHITE_NOTE_COLOR,
        black_note_color=config.BLACK_NOTE_COLOR,
        background_color=config.BACKGROUND_COLOR,
        note_color=config.NOTE_COLOR,
        dark_note_color=config.DARK_NOTE_COLOR,
        octave_lines_color=config.OCTAVE_LINES_COLOR,
        screen_height=config.SCREEN_HEIGHT,
        screen_width=config.SCREEN_WIDTH,
    )

    video_generator = VideoGenerator(
        workdir=workdir,
        midi_file_path=midi_path,
        config=video_config,
    )

    events = preprocessor.get_midi_events(midi_path)
    video_generator.generate_video(events=events, destination_filepath=video_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert midi to mp4")
    parser.add_argument("--source_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    args = parser.parse_args()

    source_path = Path(args.source_path)
    target_path = Path(args.output_path)
    assert source_path.exists(), f"File {source_path} does not exist"
    assert source_path.is_file(), f"Path {source_path} is not a file"

    convert_video(str(source_path.absolute()), str(target_path.absolute()))
