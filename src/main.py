import json
import argparse
from src.video_generator.midi_preprocessor import MidiPreprocessor
from pathlib import Path
from src.video_generator.video_generator import VideoGenerator
from utils import NoteEvent


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


def main(config, source_path: Path, video_path: Path, events_path: Path | None = None):
    preprocessor = MidiPreprocessor()
    video_generator = VideoGenerator(
        workdir=Path("workdir"),
        midi_file_path=source_path,
        config=config,
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
    parser.add_argument(
        "--config", type=str, required=False, default="config/default.json"
    )
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

    config_path = Path(args.config)
    assert config_path.exists(), f"File {config_path} does not exist"

    with open(config_path, "r") as f:
        config = json.load(f)

    main(config, source_path, target_path, events_path=events_path)
