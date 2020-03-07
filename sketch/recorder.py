from PIL import Image, ImageDraw
from pathlib import Path
from sketch.scene import Scene
from sketch.sounds import AudioSampler
from sketch.util.color import Color
from sketch.util.point import Point
from tqdm import tqdm
import cv2
import moviepy.editor as mp
import numpy as np
from typing import Dict

def image_to_array(image):
  # outputs Height x Width x Channels (weirdly whats expected)
  data = np.array(image.copy())
  # Convert colors to BGR
  data = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
  return data

class Recorder(object):
  """
  A recorder records a scene. This handles making images and merging them
  together into videos.
  """
  def __init__(
      self,
      scene:Scene,
      framerate:int,
      out_path:Path,
      canvas_size:Point,
      duration:float,
      audio_samples:Dict[str, Path]=None,
      silence_pbar=False,
      tmp_dir="/tmp"
  ):
    """
    Recorder uses scene to generate scenes that are written as a video.
    scene - The collection of entities to watch.
    framerate - frames per second
    out_path - where to put the video. Expected to be a .mp4
    canvas_size - x/y = width/height of output video
    audio_samples - name 2 audio path. Used in a Sampler to add audio.
    duration - seconds long the video is
    silence_pbar - if true, don't tqdm
    tmp_dir - used to write a mp4 and a wav. These will get merged.
    """
    tmp_dir = Path(tmp_dir)
    assert tmp_dir.is_dir(), f"Cannot find dir: {tmp_dir}"
    self.tmp_dir = tmp_dir

    self.scene = scene
    self.framerate = framerate
    self.out_path = Path(out_path)
    self.canvas_size = Point(canvas_size)
    self.duration = duration
    self.silence_pbar = silence_pbar

    assert self.framerate > 0, "Must supply positive framerate"
    assert not self.out_path.is_file(), f"Refusing to override: {out_path}"
    assert self.out_path.suffix == ".mp4", "Must write MP4 file."
    assert self.canvas_size.is_positive(), "Must supply positive canvas size."
    assert 0 < self.duration, "Invalid end time."

    self.video_writer = None
    self.timestep = 1.0/float(self.framerate)
    self.image_format = "RGBA"

    self.tmp_video = self.tmp_dir.joinpath("__video__.mp4")
    if self.tmp_video.is_file():
      print("Warning, removing", self.tmp_video)
      self.tmp_video.unlink()

    self.tmp_audio = self.tmp_dir.joinpath("__audio__.wav")
    if self.tmp_audio.is_file():
      print("Warning, removing", self.tmp_audio)
      self.tmp_audio.unlink()
    self.audio_sampler = AudioSampler(
        audio_samples=audio_samples,
        duration=duration,
        out_path=self.tmp_audio
    )


  def __enter__(self):
    self.video_writer = cv2.VideoWriter(
        str(self.tmp_video),
        cv2.VideoWriter_fourcc(*"avc1"),
        self.framerate,
        (self.canvas_size.x, self.canvas_size.y)
    )
    self.audio_sampler.clear()
    return self

  def __exit__(self, *options):
    self.video_writer.release()
    self.video_writer = None
    self.audio_sampler.export()

    mp.VideoFileClip(str(self.tmp_video)).set_audio(
      mp.AudioFileClip(str(self.tmp_audio))
    ).write_videofile(str(self.out_path))

    self.tmp_video.unlink()
    self.tmp_audio.unlink()
    return False

  def record(self):
    """
    Actually runs the scene, makes a frame, draws the frame, outputs results.
    """
    assert self.video_writer is not None, "Record called outside of context"
    pbar = tqdm(total=self.duration, disable=self.silence_pbar)
    # we're going to constantly write to this
    frame = Image.new(
        self.image_format,
        (self.canvas_size.x, self.canvas_size.y),
    )
    draw_ctx = ImageDraw.Draw(frame)
    while self.scene.clock < self.duration:
      self.scene.step(self.timestep, audio_sampler=self.audio_sampler)
      pbar.update(self.timestep)
      self.scene.draw(draw_ctx)
      frame_data = image_to_array(frame)
      self.video_writer.write(frame_data)
