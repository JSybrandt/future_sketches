#!/usr/bin/env python3

from fire import Fire
from pathlib import Path
from sketch.util.point import Point
from sketch.util.color import Color
from sketch.entities.entity import Entity
from sketch.recorder import Recorder
from sketch.scene import Scene
from random import random

class Bouner(Entity):
  def __init__(self, start:Point, canvas_size:Point, speed:float, width:float=10):
    Entity.__init__(self, position=start)
    self.width = width
    self._half_width = Point(self.width/2, self.width/2)
    self.color = Color.Random()
    self.direction = Point.RandomDirection()
    self.canvas_size = canvas_size
    self.speed = speed

  def step(self, timestep, scene, audio_sampler):
    assert self.position is not None
    assert self.canvas_size is not None
    self.position += self.direction * self.speed * timestep
    collide = False
    if self.position.x <= 0 or self.position.x >= self.canvas_size.x:
      self.position.x = max(min(self.position.x, self.canvas_size.x), 0)
      self.direction.x *= -1
      collide = True
    if self.position.y <= 0 or self.position.y >= self.canvas_size.y:
      self.position.y = max(min(self.position.y, self.canvas_size.y), 0)
      self.direction.y *= -1
      collide = True
    if collide:
      self.color = Color.Random()
      audio_sampler.trigger("coin", scene.clock)

  def draw(self, draw_ctx):
    top_left = self.position - self._half_width
    bot_right = self.position + self._half_width
    draw_ctx.ellipse(
        (top_left.x, top_left.y, bot_right.x, bot_right.y),
        fill=self.color.to8bit_rgba()
    )


def video_test(
    canvas_width=1900,
    canvas_height=1080,
    out_path="test.mp4",
    framerate=30,
    num=100,
    duration=5
):
  out_path = Path(out_path)
  canvas_size = Point(canvas_width, canvas_height)
  background_color = Color(r=0.2, g=0.4, b=0.8)


  bouncers = [
    Bouner(
      start=Point.Random(canvas_size),
      speed = 100 + random() * 500,
      width = 10 + random() * 50,
      canvas_size=canvas_size,
    )
    for _ in range(num)
  ]

  scene = Scene(
      canvas_size=canvas_size,
      background_color=None,
  )
  scene.entities = bouncers
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

