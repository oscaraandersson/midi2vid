from __future__ import annotations
from typing import Dict
import os
import pygame
from tqdm import tqdm

from pathlib import Path
from src.utils import NoteEvent

import logging
import time
from functools import wraps
from src.config import Config
from src.video_generator.piano import Piano, Note
from src.video_generator.note_animation import NoteAnimation


config = Config()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class VideoGeneratorConfig:
    def __init__(
        self,
        bpm,
        fps,
        speed,
        ticks_per_beat,
        white_note_color,
        black_note_color,
        background_color,
        octave_lines_color,
        note_color,
        dark_note_color,
        screen_width,
        screen_height,
    ):
        self.bpm = bpm
        self.fps = fps
        self.speed = speed

        # colors keys
        self.white_note_color = white_note_color
        self.black_note_color = black_note_color

        self.background_color = background_color
        self.octave_lines_color = octave_lines_color

        # falling notes standrad notes
        self.note_color = (179, 44, 49)
        self.dark_note_color = (113, 34, 36)

        # right and left hand
        self.right_note_color = (168, 255, 145)
        self.left_note_color = (176, 202, 229)
        self.dark_right_note_color = (118, 208, 68)
        self.dark_left_note_color = (124, 142, 151)

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.note_animation = NoteAnimation(
            bpm=bpm,
            fps=fps,
            ticks_per_beat=ticks_per_beat,
            screen_height=screen_height,
            note_speed=self.speed,
        )


def log_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        logging.info(f"{func.__name__} took {execution_time:.4f} ms")
        return result

    return wrapper


class VideoGenerator:
    """Generates a video of notes in a midi file"""

    def __init__(
        self,
        workdir: Path,
        midi_file_path: Path,
        config: VideoGeneratorConfig,
    ):
        self.workdir = workdir
        self.framedir = workdir / "frames"
        self.config: VideoGeneratorConfig = config
        self.midi_file_path = midi_file_path
        self.piano = Piano(
            screen_width=config.screen_width, screen_height=config.screen_height
        )

        # TODO: Map the note to a bool so we can set the right or left hand color
        self.active_notes: Dict[int, None | NoteEvent] = {
            i: None for i in self.piano.midi_key_range
        }
        self._setup_workdir()

    def _setup_workdir(self):
        if not self.workdir.exists():
            raise FileNotFoundError(f"Workdir {str(self.workdir)} does not exist")
        if not self.midi_file_path.exists():
            raise FileNotFoundError(
                f"Midi file {str(self.midi_file_path)} does not exist"
            )
        print(self.framedir)
        self.framedir.mkdir()

    def _render_frames(self):
        os.system(
            f"ffmpeg -framerate {self.config.fps} -i {self.framedir}/%5d.jpg \
                -c:v libx264 \
                -r {self.config.fps} \
                {self.framedir}/video-no-sound.mp4"
        )

    def _render_audio(self):
        os.system(
            f"fluidsynth -ni {str(config.SOUND_FONT_PATH.absolute())} \
                {self.midi_file_path} \
                -F {self.workdir}/audio.wav"
        )

    def _merge_audio_and_video(self, destination_filepath: Path):
        os.system(
            f"ffmpeg -y -i {self.framedir}/video-no-sound.mp4 \
                -i {self.workdir}/audio.wav -c:v copy \
                -c:a aac -strict experimental \
                -b:a 192k -f mp4 {destination_filepath.absolute()}"
        )

    def _draw_vertical_lines(self, screen, screen_height):
        left_positions = []
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

    def _draw_piano(self, screen):
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
                    # if hand is not set, it means it's a note that is played by both hands
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

    def _save_frame(self, path, screen, frame_number):
        pygame.image.save(screen, f"{path}/{frame_number:05}.jpg")

    def _is_active(self, note_position, duration, midi_note_id):
        white_key_height_relative_bottom = (
            self.config.screen_height - self.piano.white_key_height
        )
        if (
            note_position > white_key_height_relative_bottom
            and (note_position - duration) < white_key_height_relative_bottom
        ):
            return True

    def _draw_note(self, note_event, frame_id, screen):
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
            self.config.note_animation.get_note_position(
                note_event.start, frame_id, int(self.piano.white_key_height)
            )
        )  # the top of the note relative to the top of the screen which is 0

        left_pos = (
            self.piano.get_left_key_pos(note, white_key_width, black_key_width)
            + note_padding
        )
        # darw the note
        duration = self.config.note_animation.get_note_length(
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

    def _generate_frames2(self, events: list[NoteEvent]):
        """Use a different approach to generate frames. This approach should be parallelized
        all noteposistions should be determined by the frame number
        """
        screen = pygame.Surface((self.config.screen_width, self.config.screen_height))
        pygame.init()

        total_frames = self.config.note_animation.get_total_number_of_frames(events)

        for frame_id in tqdm(
            range(total_frames),
            desc="Generating frames",
            unit="frame",
            total=total_frames,
        ):
            # reset active notes
            self.active_notes = {note: None for note in self.piano.midi_key_range}
            screen.fill(self.config.background_color)
            # select the events that are in the current frame
            active_events: list[NoteEvent] = (
                self.config.note_animation.get_active_note_events(
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

    @log_performance
    def generate_video(
        self, events: list[NoteEvent], destination_filepath: Path, sample=False
    ):
        logging.info("Generating frames")
        self._generate_frames2(events)
        logging.info("Rendering video")
        self._render_frames()
        logging.info("Rendering audio")
        self._render_audio()
        logging.info("Merging audio and video")
        self._merge_audio_and_video(destination_filepath)
