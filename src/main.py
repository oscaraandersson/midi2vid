import os
import json
import argparse
from src.video_generator.midi_preprocessor import MidiPreprocessor
from pathlib import Path
import os
from src.video_generator.video_generator import VideoGeneratorConfig
from src.video_generator.video_generator import VideoGenerator
from src.config import Config
from utils import NoteEvent


config = Config()


def read_events(events_path: Path) -> list[NoteEvent]:
    """
    Read events from a json file. The file should have the following format:
    [
        {note: int, velocity: int, start: int, end: int, hand: str},
    ]
    """
    print(events_path)
    with open(events_path, "r") as f:
        events_raw = json.load(f)
    events = []
    for event in events_raw:
        e = NoteEvent(
            note=event["note"],
            velocity=event["velocity"],
            start=event["start"],
            end=event["end"],
            hand=event["hand"],
        )
        events.append(e)
    return events


def convert_video(source_path: Path, video_path: Path, events_path: Path | None = None):
    workdir = Path("workdir")
    if workdir.exists():
        os.system("rm -rf workdir")
    workdir.mkdir(parents=True, exist_ok=False)

    preprocessor = MidiPreprocessor()

    video_config = VideoGeneratorConfig(
        bpm=config.BPM,
        fps=config.FPS,
        speed=config.SPEED,
        ticks_per_beat=preprocessor.get_ticks_per_beat(source_path),
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
        midi_file_path=source_path,
        config=video_config,
    )

    events = []
    if events_path:
        events = read_events(events_path)
        print(len(events))
    else:
        events = preprocessor.get_midi_events(source_path)
        print(len(events))
    video_generator.generate_video(events=events, destination_filepath=video_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert midi to mp4")
    parser.add_argument("--source_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--events_path", type=str, required=False)
    args = parser.parse_args()

    source_path = Path(args.source_path)
    target_path = Path(args.output_path)
    assert source_path.exists(), f"File {source_path} does not exist"
    assert source_path.is_file(), f"Path {source_path} is not a file"

    source_path = Path(args.source_path)
    target_path = Path(args.output_path)
    events_path = Path(args.events_path) if args.events_path else None
    assert source_path.exists(), f"File {source_path} does not exist"
    assert source_path.is_file(), f"Path {source_path} is not a file"

    convert_video(source_path, target_path, events_path=events_path)
