import pydub
from sketch.sounds import sec_to_mil

def fade_out(
    duration:float,
)->pydub.AudioSegment:
  """
  Applies a fade to nothing over the last duration seconds.
  """
  return lambda seg: seg.fade_out(sec_to_mil(duration))

def fade_in(
    duration:float,
)->pydub.AudioSegment:
  """
  Applies a fade to nothing over the last duration seconds.
  """
  return lambda seg: seg.fade_in(sec_to_mil(duration))

def fade_in_and_out(
    in_duration:float,
    out_duration:float,
)->pydub.AudioSegment:
  return lambda seg: (
      seg.fade_in(
        sec_to_mil(in_duration)
      ).fade_out(
        sec_to_mil(out_duration)
      )
  )
