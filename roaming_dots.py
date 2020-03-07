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

  entities = [
    PhysicsCircle(
      radius=25,
      velocity=Point.Right() * 100,
      position=Point(100, 110)
    ),
    PhysicsCircle(
      radius=25,
      velocity=Point.Left() * 100,
      position=Point(500, 100)
    ),
    PhysicsCircle(
      radius=25,
      velocity=Point.Right() * 100,
      position=Point(100, 500)
    ),
    MusicBox(
      size=Point(150,50),
      angle=math.pi/4,
      position=Point(500, 500),
      color=Color(1,0,0),
      audio_sample_name="coin"
    ),
    PhysicsCircle(
      radius=10,
      color=Color(0,1,0),
      acceleration=Point.Down()*100,
      position=Point(500, 325),
    ),
  ]

  for entity in entities:
    entity.collides_with = entities

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
        "coin": "./sounds/coin.mp3"
      },
  )

  with recorder:
    recorder.record()


if __name__ == "__main__":
  Fire(video_test)

