from mido.midifiles.midifiles import MidiFile
from src.utils import NoteEvent
from collections import defaultdict
from pathlib import Path


class MidiPreprocessor:
    def __init__(self):
        self.events = []

    def _initialize_note(self, temp, msg, time):
        temp_note = NoteEvent(msg.note, msg.velocity, time)
        temp[msg.note] = temp_note

    def _handle_note_off(self, temp, msg, time):
        for note in temp.values():
            if not note:
                continue
            elif note.end == None and note.note == msg.note:
                note.set_end(time)
                self.events.append(note)
                temp[msg.note] = None

    def _preprocess_track(self, track):
        time = 0  # the cumalative time accross the whole song
        active_notes = {}
        for _, msg in enumerate(track):
            time += msg.time
            if not msg.type == "note_on":
                continue
            if msg.velocity != 0:  # we have a starting note
                self._initialize_note(active_notes, msg, time)
            else:  # note on with velocity 0 is the same as note off
                self._handle_note_off(active_notes, msg, time)

    def _extract_midi_objects(self, midi_path):
        # read the midifile with mido
        mid = MidiFile(midi_path)
        for track in mid.tracks:
            self._preprocess_track(track)
        self.events = sorted(self.events, key=lambda x: x.start)

    def _trim_long_notes(self, max_note_length: int):
        """Trim notes that are longer than max_note_length
        max_note_length: the maximum duration of a note in ticks
        """
        for i in range(len(self.events)):
            self.events[i].trim_note(max_note_length)

    def _fix_sequential_notes(self):
        def _init_node():
            note = NoteEvent(0, 0, 0)
            note.set_end(0)
            return note

        previous_note_map = defaultdict(lambda: _init_node())
        for i in range(len(self.events)):
            current_note = self.events[i]
            if previous_note_map[current_note.note].end > current_note.start:
                previous_note_map[current_note.note].end = current_note.start - 50
            previous_note_map[current_note.note] = current_note

    def get_midi_events(self, midi_path: Path, max_note_length: int) -> list[NoteEvent]:
        self._extract_midi_objects(midi_path)
        self._trim_long_notes(max_note_length=max_note_length)
        self._fix_sequential_notes()
        return self.events

    def get_ticks_per_beat(self, midi_path: Path) -> int:
        mid = MidiFile(midi_path)
        return mid.ticks_per_beat
