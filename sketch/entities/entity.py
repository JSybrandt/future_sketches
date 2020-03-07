from abc import ABC
from abc import abstractmethod
from PIL.ImageDraw import Draw
from sketch.util.point import Point
from sketch.sounds import AudioSampler


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
  ):
    self.visible = visible
    self.active = active
    if position is None:
      self.position = Point(0, 0)
    else:
      self.position = position.copy()
    self.z_order = z_order
    self.action_order = action_order

  @abstractmethod
  def draw(self, draw_ctx:Draw):
    """
    Draws the entity on the image.
    """
    pass

  @abstractmethod
  def step(self, timestep:float, scene, audio_sampler):
    """
    Updates internal parameters of the entity based on time step.
    """
    pass

  def move(self, delta:Point):
    self.position += delta

  def put(self, position:Point):
    self.position = position.copy()
