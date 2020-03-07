from PIL.ImageDraw import Draw
from abc import ABC
from abc import abstractmethod
from sketch.sounds import AudioSampler
from sketch.util.point import Point
from sketch.util.color import Color
from typing import Union, List, Tuple, Optional
import collision


class Entity(ABC):
  """
  An entity is something that is displayed on screen and updated every frame.
  """

  def __init__(
      self,
      position=None,
      visible=True,
      active=True,
      z_order:float=0,
      action_order:float=0,
      collision_shape:Union[collision.Circle, collision.Poly]=None,
      collides_with:List[object]=None,
      color=None,
      angle=0,
  ):
    self.visible = visible
    self.active = active
    if position is None:
      self.position = Point(0, 0)
    else:
      self.position = position.copy()
    self.z_order = z_order
    self.action_order = action_order
    self.collision_shape=collision_shape
    if collides_with is None:
      self.collides_with = []
    else:
      self.collides_with = collides_with
    self.angle = angle
    # Child classes set this to true if needed
    self._needs_collision_response = False
    if color is None:
      # Default color is white
      self.color = Color(1,1,1)
    else:
      self.color = color

  ## The following stubs are listed in order of calls per-frame

  @abstractmethod
  def step(self, timestep:float, scene, audio_sampler):
    """
    How does this entity move each frame?
    """
    pass

  # Optional Override
  def pre_collision(self)->None:
    """
    Gives the entity a chance to update collision object parameters.
    """
    if self.collision_shape is not None:
      self.collision_shape.pos.set(self.position)
      if hasattr(self.collision_shape, "angle"):
        self.collision_shape.angle = self.angle

  # Optional Override
  def on_collision(self, other, response:Optional[collision.Response])->None:
    """
    If this entity collides with another, update information.
    Note, don't update the actual location of this entity until post_collision.
    """
    pass

  # Optional Override
  def post_collision(self)->None:
    """
    After all collisions have happened, take a step in response.
    """
    pass

  @abstractmethod
  def draw(self, draw_ctx:Draw):
    """
    Draws the entity on the image. Called after all steps.
    """
    pass

  ## End stubs

  def move(self, delta:Point):
    self.position += delta

  def put(self, position:Point):
    self.position = position.copy()

  def check_collision(self, other)->Tuple[bool, Optional[collision.Response]]:
    collided = False
    response = None
    if other is not self:
      if self._needs_collision_response:
        response = collision.Response()
      if self.collision_shape is not None and other.collision_shape is not None:
        # module function to check collision btwn shapes
        collided = collision.collide(
            self.collision_shape,
            other.collision_shape,
            response=response
        )
    return collided, response

  def check_collisions(self)->None:
    """
    Checks all collisions against partners and performs on_collision.
    """
    for other in self.collides_with:
      if other.active:
        collides, response = self.check_collision(other)
        if collides:
          self.on_collision(other, response)


