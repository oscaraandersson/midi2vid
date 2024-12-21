from __future__ import annotations


class CustomMessage:
  """Abstratction of a message
  Notes can be defined from start to end instead of the start being defined
  relative to the previous message. This makes it easier to change the
  duration of the notes
  """

  def __init__(self, start: int):
    self.start = start
    self.end: int = 0

  def set_end(self, end: int):
    self.end = end - self.start

  def trim_note(self, duration: int):
    self.end = self.start + duration


class NoteEvent(CustomMessage):
  def __init__(
    self,
    note: int,
    velocity: int,
    start: int,
    end: int = 0,
    hand: str | None = None,
  ):
    super().__init__(start)
    self.note = note
    self.velocity = velocity
    self.end = end
    self.hand = hand

  def get_start(self):
    return NoteEvent(self.note, self.velocity, self.start)


class Pedal(CustomMessage):
  PEDAL_CONTROL = 64

  def __init__(self, start: int, value: int):
    super().__init__(start)
    self.value = value

  def set_end(self, end: int):
    self.end = end

  def get_start(self):
    return Pedal(self.start, self.value)
