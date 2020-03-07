from sketch.entities.entity import Entity
from sketch.util.point import Point
from sketch.util.color import Color
from typing import List, Optional
from PIL.ImageDraw import Draw
from sketch.sounds import AudioSampler

class Scene(object):
  """
  A scene is something that updates and draws entities each frame.
  """
  def __init__(
      self,
      canvas_size:Point,
      background_color:Optional[Color]=None,
      entities:List[Entity]=None,
  ):
    if entities is not None:
      self.entities = entities
    else:
      self.entities = []
    if background_color is None:
      # indicates not to clear between frames
      self.background_color = None
    else:
      self.background_color = background_color.copy()
    self.canvas_size = canvas_size.copy()
    self._clock = 0
    self._ordered = False

  @property
  def clock(self):
    return self._clock

  def step(self, timestep:float, audio_sampler:AudioSampler):
    self._establish_order()
    self._clock += timestep
    # All Step
    for entity in self.action_order:
      if entity.active:
        entity.step(timestep=timestep, scene=self, audio_sampler=audio_sampler)
    # All prepare for collisions
    for entity in self.action_order:
      if entity.active:
        entity.pre_collision()
    # All check collisions
    for entity in self.action_order:
      if entity.active:
        entity.check_collisions()
    # Update based on collisions
    for entity in self.action_order:
      if entity.active:
        entity.collision_step(
            timestep=timestep,
            scene=self,
            audio_sampler=audio_sampler
        )



  def draw(self, draw_ctx:Draw):
    self._establish_order()
    if self.background_color is not None:
      draw_ctx.rectangle(
        [(0, 0), tuple(self.canvas_size+(1,1))],
        fill=self.background_color.to8bit_rgba()
      )
    for entity in self.z_order:
      if entity.visible:
        entity.draw(draw_ctx)

  def add_entity(self, entity:Entity):
    self.entities.append(entity)
    self._ordered = False

  def _establish_order(self):
    if not self._ordered:
      self.action_order = sorted(self.entities, key=lambda e: e.action_order)
      self.z_order = sorted(self.entities, key=lambda e: e.z_order)
      self._ordered = True
