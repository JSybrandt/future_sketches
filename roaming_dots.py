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
  edge_box_width = 50
  high_hat_margin = 200

  circles = [
    PhysicsCircle(
      radius=radius,
      velocity=Point.RandomDirection() * 500,
      position=(
        Point.Random(
          bounds=(canvas_width-100, canvas_height-100)
        )
        + (50, 50)
      ),
      color=Color.Random()
    )
    for _  in range(5)
  ]

  music_boxes = [
    MusicBox(
      size=Point(edge_box_width, canvas_height),
      position=Point(edge_box_width/2, canvas_height/2),
      color=Color(1,0,0),
      audio_sample_name="kick",
    ),
    MusicBox(
      size=Point(edge_box_width, canvas_height),
      position=Point(canvas_width-edge_box_width/2, canvas_height/2),
      color=Color(1,0,0),
      audio_sample_name="kick",
    ),
    MusicBox(
      size=Point(canvas_width, edge_box_width),
      position=Point(canvas_width/2, edge_box_width/2),
      color=Color(1,1,0),
      audio_sample_name="snare",
    ),
    MusicBox(
      size=Point(canvas_width, edge_box_width),
      position=Point(canvas_width/2, canvas_height-edge_box_width/2),
      color=Color(1,1,0),
      audio_sample_name="snare",
    ),

    MusicBox(
      size=Point(edge_box_width/4, 2*edge_box_width),
      position=Point(high_hat_margin, high_hat_margin),
      angle=math.pi/4,
      color=Color(.5,1,.5),
      audio_sample_name="high_hat_closed",
    ),
    MusicBox(
      size=Point(edge_box_width/4, 2*edge_box_width),
      position=Point(high_hat_margin, canvas_height-high_hat_margin),
      angle=-math.pi/4,
      color=Color(.5,1,.5),
      audio_sample_name="high_hat_closed",
    ),
    MusicBox(
      size=Point(edge_box_width/4, 2*edge_box_width),
      position=Point(canvas_width-high_hat_margin, high_hat_margin),
      angle=-math.pi/4,
      color=Color(.5,1,.5),
      audio_sample_name="high_hat_closed",
    ),
    MusicBox(
      size=Point(edge_box_width/4, 2*edge_box_width),
      position=Point(canvas_width-high_hat_margin, canvas_height-high_hat_margin),
      angle=math.pi/4,
      color=Color(.5,1,.5),
      audio_sample_name="high_hat_closed",
    ),
  ]

  for c in circles:
    c.collides_with += music_boxes
    c.collides_with += circles
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

