from sketch.entities.physics_entity import PhysicsRectangle
from sketch.entities.physics_entity import to_collision_rect
import collision
from sketch.sounds import SoundDescription
from random import choice

class MusicBox(PhysicsRectangle):
  """
  The music box does not move, but makes a sound whenever something collides
  with it. Plays a random selection of its internal sounds.
  """
  def __init__(self, sounds:SoundDescription, **kwargs):
    PhysicsRectangle.__init__(self, **kwargs)
    self.frozen=True
    self.sounds = sounds
    self._collided_this_frame = False
    # Used to animate a "bounce"
    self._scale = 1.0
    self._scale_rate = 1
    self._on_collision_scale = 1.2


  def step(self, timestep, scene, audio_sampler)->None:
    PhysicsRectangle.step(self, timestep, scene, audio_sampler)
    if self._scale > 1:
      self._scale -= self._scale_rate * timestep
    if self._scale < 1:
      self._scale = 1

  def pre_collision(self)->None:
    PhysicsRectangle.pre_collision(self)
    self._collided_this_frame = False

  def on_collision(self, *args, **kwargs)->None:
    PhysicsRectangle.on_collision(self, *args, **kwargs)
    self._collided_this_frame = True

  def collision_step(self, timestep, scene, audio_sampler)->None:
    PhysicsRectangle.collision_step(self, timestep, scene, audio_sampler)
    if self._collided_this_frame:
      sound = choice(self.sounds)
      audio_sampler.trigger(sound, scene.clock)
      self._scale = self._on_collision_scale

  def draw(self, draw_ctx)->None:
    if self._scale == 1:
      draw_ctx.polygon(
          [(p.x, p.y) for p in self.collision_shape.points],
          fill=self.color.to8bit_rgba()
      )
    else:
      draw_ctx.polygon(
          [
            (p.x, p.y) for p in
            to_collision_rect(
              size=self.size * self._scale,
              position=self.position,
              angle=self.angle
            ).points
          ],
          fill=self.color.to8bit_rgba()
      )
