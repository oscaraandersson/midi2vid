from __future__ import annotations


class CustomMessage:
    """Abstratction of a message
    Notes can be defined from start to end instead of the start being defined
    relative to the previous message. This makes it easier to change the
    duration of the notes
    """

    def __init__(self, start):
        self.start = start
        self.end: int | None = None

    def set_end(self, end):
        self.end = end - self.start

    def trim_note(self, duration):
        self.end = self.start + duration


class NoteEvent(CustomMessage):
    def __init__(self, note, velocity, start, hand=None):
        super().__init__(start)
        self.note = note
        self.velocity = velocity

    def get_start(self):
        return NoteEvent(self.note, self.velocity, self.start)

    def get_end(self):
        return NoteEvent(self.note, 0, self.end)


class Pedal(CustomMessage):
    PEDAL_CONTROL = 64

    def __init__(self, start, value):
        super().__init__(start)
        self.value = value

    def set_end(self, end):
        self.end = end

    def get_start(self):
        return Pedal(self.start, self.value)

    def get_end(self):
        return Pedal(self.end, 0)
