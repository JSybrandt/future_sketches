import pydub
from pydub.generators import SignalGenerator
from pathlib import Path
from typing import Dict, Callable
import math

def pitch_to_frequency(pitch:int)->float:
  assert 0 <= pitch <= 88, "Pitch is one of 88 keyboard keys"
  return 440 * 2 ** ((pitch-49)/12)

def sec_to_mil(seconds:float):
  return int(seconds * 1000)

class SoundDescription(object):
  def __init__(self):
    self.audio_segments = []
    # Used to cache get_sound
    self.sound = None

  def add_sample(
      self,
      sample_path:Path,
      volume:float=0,
      duration:float=None,
  ):
    """
    Adds a prerecorded sample to the description.
    Volume corresponds to DB, with 0 being the loudest.
    Duration is the number of seconds to cut the clip to.
    """
    sample_path = Path(sample_path)
    assert sample_path.is_file(), "Cannot find audio sample."
    assert duration is None or duration > 0, "Must have positive duration."

    sample = pydub.AudioSegment.from_file(sample_path)
    sample += volume
    if duration is not None and len(sample) > sec_to_mil(duration):
      sample = sample[:sec_to_mil(duration)]
    self.audio_segments.append(sample)
    self.sound = None
    return self

  def add_generator(
      self,
      generator:SignalGenerator,
      duration:float,
      volume:float=0,
      effect:Callable[[pydub.AudioSegment], pydub.AudioSegment]=None
  )->None:
    seg = generator.to_audio_segment(
        duration=sec_to_mil(duration),
        volume=volume
    )
    if effect is not None:
      seg = effect(seg)
    self.audio_segments.append(
        seg
    )
    self.sound = None
    return self

  def get_sound(self)->pydub.AudioSegment:
    assert len(self.audio_segments) > 0, "Called overlay with no segments."
    if self.sound is None:
      # Total duration equal to longest segment
      duration = max(map(len, self.audio_segments))
      self.sound = pydub.AudioSegment.silent(duration=duration)
      for seg in self.audio_segments:
        self.sound = self.sound.overlay(seg, position=0)
    return self.sound


class AudioSampler(object):
  """
  This class plays audio_samples from a collection at specific times. It can output
  its results to a file.
  """

  def __init__(
      self,
      duration:float,
      out_path:Path,
  ):
    """
    Samples must all be named.
    """
    assert duration > 0, f"Invalid duration"
    assert not out_path.exists(), f"Refusing to overwrite {out_path}"
    self.out_path = out_path
    self.base = pydub.AudioSegment.silent(duration=sec_to_mil(duration))

  def trigger(self, sound_desc:SoundDescription, when:float)->None:
    """
    Triggers the sample at 'when' seconds into the base.
    """
    self.base = self.base.overlay(
        sound_desc.get_sound(),
        position=sec_to_mil(when)
    )

  def export(self)->None:
    assert not self.out_path.exists(), \
        f"Refusing to overwrite: {self.out_path}"
    self.base.export(self.out_path)

  def clear(self)->None:
    self.base = pydub.AudioSegment.silent(duration=len(self.base))
