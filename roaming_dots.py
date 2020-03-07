#!/usr/bin/env python3

from fire import Fire
from pathlib import Path
from sketch.util.point import Point
from sketch.util.color import Color
from sketch.entities.physics_entity import PhysicsCircle
from sketch.entities.music_box import MusicBox
from sketch.recorder import Recorder
from sketch.scene import Scene
from random import random
import math



def video_test(
    canvas_width=800,
    canvas_height=600,
    out_path="test.mp4",
    framerate=30,
    duration=10
):
  out_path = Path(out_path)
  canvas_size = Point(canvas_width, canvas_height)
  background_color = Color(r=0.2, g=0.4, b=0.8)

  radius = 20
  left = 100

  high_hat_delta = (canvas_width - 200) / 2
  base_drum_delta = high_hat_delta * 2


  circles = [
    # Hits base drums
    PhysicsCircle(
      radius=radius,
      velocity=Point.Left() * canvas_width,
      position=Point(left+radius, canvas_height/4)
    ),
    # Hits high hats
    PhysicsCircle(
      radius=radius,
      velocity=Point.Left() * canvas_width,
      position=Point(left+radius, 3*canvas_height/4)
    ),
  ]

  music_boxes = [
    MusicBox(
      size=Point(100,200),
      position=Point(left-50, canvas_height/4),
      color=Color(1,0,0),
      audio_sample_name="kick"
    ),
    MusicBox(
      size=Point(50,150),
      position=Point(left+25+base_drum_delta+2*radius, canvas_height/4),
      color=Color(1,0,1),
      audio_sample_name="snare"
    ),

    MusicBox(
      size=Point(30,100),
      position=Point(left-15, 3*canvas_height/4),
      color=Color(1,1,0),
      audio_sample_name="high_hat_closed"
    ),
    MusicBox(
      size=Point(30,100),
      position=Point(left+15+high_hat_delta+2*radius, 3*canvas_height/4),
      color=Color(1,1,0),
      audio_sample_name="high_hat_closed"
    ),
  ]

  for c in circles:
    c.collides_with += music_boxes
  for b in music_boxes:
    b.collides_with += circles

  entities = circles + music_boxes

  scene = Scene(
      canvas_size=canvas_size,
      background_color=Color(0,0,0),
      entities=entities,
  )

  recorder = Recorder(
      scene=scene,
      framerate=framerate,
      out_path=out_path,
      canvas_size=canvas_size,
      duration=duration,
      audio_samples={
        "coin": "./sounds/coin.mp3",
        "kick": "./sounds/kick.mp3",
        "snare": "./sounds/snare.wav",
        "high_hat_closed": "./sounds/high_hat_closed.wav",
      },
  )

  with recorder:
    recorder.record()


if __name__ == "__main__":
  Fire(video_test)

