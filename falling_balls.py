#!/usr/bin/env python3

from fire import Fire
from pathlib import Path
from pydub.generators import Sine
from sketch.util.point import Point
from sketch.util.color import Color
from sketch.entities.physics_entity import PhysicsCircle
from sketch.entities.music_box import MusicBox
from sketch.recorder import Recorder
from sketch.scene import Scene
from sketch.sounds import SoundDescription
from sketch.sounds import pitch_to_frequency
from sketch.sound_effects import fade_in_and_out
from sketch.entities.falling_ball import FallingBall
from random import random
import math



def main(
    canvas_width=800,
    canvas_height=800,
    out_path="test.mp4",
    framerate=60,
    duration=20
):
  out_path = Path(out_path)
  canvas_size = Point(canvas_width, canvas_height)
  background_color = Color(r=0.2, g=0.4, b=0.8)

  spawn_height = 400
  spawn_rect = [(0, -spawn_height), (canvas_width, spawn_height)]
  alive_rect = [(-100, -100), (canvas_width+200, canvas_height+200)]
  gravity = Point.Down() * 300
  ball_radius = 15
  num_balls = 20
  box_size = 75
  box_rotation = math.pi / 4
  horizintal_spacing = canvas_width/5
  vertical_spacing = canvas_height/5
  horizintal_margin = canvas_width/5
  vertical_margin = canvas_width/5

  falling_balls = [
      FallingBall(
        spawn_rect=spawn_rect,
        alive_rect=alive_rect,
        radius=ball_radius,
        acceleration=gravity,
        color=Color.Random(),
      )
      for _ in range(num_balls)
  ]

  notes = [
      SoundDescription().add_generator(
        Sine(freq=pitch_to_frequency(pitch)),
        volume=-15,
        duration=0.3,
        effect=fade_in_and_out(0.1, 0.2)
      ) for pitch in [
        #16, # c2
        #18, 20, 23, 25,
        28, # c3
        30, 32, 35, 38,
        40, # c4
        42, 44, 47, 50,
        52, # c5
        54, 56, 59, 62,
        64, # c6
      ]
  ]
  positions = []
  for x in range(4):
    for y in range(4):
      offset = 0
      if y % 2 == 0:
        offset += horizintal_spacing/2
      positions.append(
          Point(
            x*horizintal_spacing + horizintal_margin + offset,
            y*vertical_spacing + vertical_margin
          )
      )

  music_boxes = [
    MusicBox(
      size=Point(box_size, box_size),
      angle=random()*math.pi,
      position=pos,
      color=Color(
        pos.x/canvas_width,
        pos.y/canvas_height,
        pos.x/canvas_width
      ),
      sounds=[note]
    )
    for pos, note in zip(positions, notes)
  ]
  for ball in falling_balls:
    ball.collides_with += music_boxes
  for box in music_boxes:
    box.collides_with += falling_balls
  entities = falling_balls + music_boxes

  scene = Scene(
      canvas_size=canvas_size,
      background_color=background_color,
      entities=entities,
  )

  recorder = Recorder(
      scene=scene,
      framerate=framerate,
      out_path=out_path,
      canvas_size=canvas_size,
      duration=duration,
  )

  with recorder:
    recorder.record()


if __name__ == "__main__":
  Fire(main)

