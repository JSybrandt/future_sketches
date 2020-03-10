from sketch.entities.physics_entity import PhysicsCircle
from sketch.entities.physics_entity import to_collision_rect
from random import random
from typing import Tuple
from sketch.util.point import Point
import collision

class FallingBall(PhysicsCircle):
  """
    Falling balls start in a random location within the spawning rectangle.
    They travel using the standard physics circle pattern of
    velocity and acceleration. Once they leave the spawn rectangle, they die
    unless they are touching the alive rectangle.
  """
  def __init__(
    self,
    spawn_rect:Tuple[Point, Point],  # x, y, width, height
    alive_rect:Tuple[Point, Point],
    **kwargs
  ):
    PhysicsCircle.__init__(self, **kwargs)
    assert len(spawn_rect) == 2, "Rectangle is two points"
    assert len(alive_rect) == 2, "Rectangle is two points"
    self.spawn_rect = tuple(Point(p) for p in spawn_rect)
    self.alive_rect = tuple(Point(p) for p in alive_rect)
    self._spawn_collision_shape = to_collision_rect(
      position=self.spawn_rect[0] + self.spawn_rect[1]/2,
      size=self.spawn_rect[1],
    )
    self._alive_collision_shape = to_collision_rect(
      position=self.alive_rect[0] + self.alive_rect[1]/2,
      size=self.alive_rect[1],
    )
    self._init_velocity = self.velocity.copy()
    self._init_acceleration = self.acceleration.copy()
    self.respawn()

  def respawn(self)->None:
    self.put(
        self.spawn_rect[0] + Point.Random(self.spawn_rect[1])
    )
    self.velocity = self._init_velocity.copy()
    self.acceleration = self._init_acceleration.copy()

  def collision_step(self, timestep, scene, audio_sampler)->None:
    PhysicsCircle.collision_step(self, timestep, scene, audio_sampler)
    in_spawn_zone = collision.collide(
        self.collision_shape,
        self._spawn_collision_shape,
    )
    if not in_spawn_zone:
      in_alive_zone = collision.collide(
        self.collision_shape,
        self._alive_collision_shape
      )
      if not in_alive_zone:
        self.respawn()

