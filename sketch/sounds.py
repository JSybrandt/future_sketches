import pydub
from pathlib import Path
from typing import Dict

def sec_to_mil(seconds:float):
  return int(seconds * 1000)

class AudioSampler(object):
  """
  This class plays audio_samples from a collection at specific times. It can output
  its results to a file.
  """

  def __init__(
      self,
      audio_samples:Dict[str, Path],
      duration:float,
      out_path:Path,
  ):
    """
    Samples must all be named.
    """
    assert duration > 0, f"Invalid duration"
    assert not out_path.exists(), f"Refusing to overwrite {out_path}"
    self.out_path = out_path

    self.name2sample = {}
    for name, path in audio_samples.items():
      self.name2sample[name] = pydub.AudioSegment.from_file(path)
    self.base = pydub.AudioSegment.silent(duration=sec_to_mil(duration))

  def trigger(self, sample_name:str, when:float)->None:
    """
    Triggers the sample at 'when' seconds into the base.
    """
    assert sample_name in self.name2sample, f"Invalid sample name:{sample_name}"
    self.base = self.base.overlay(
        self.name2sample[sample_name],
        position=sec_to_mil(when)
    )

  def export(self)->None:
    assert not self.out_path.exists(), \
        f"Refusing to overwrite: {self.out_path}"
    self.base.export(self.out_path)

  def clear(self)->None:
    self.base = pydub.AudioSegment.silent(duration=len(self.base))
