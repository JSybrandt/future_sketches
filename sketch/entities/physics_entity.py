from sketch.entities.entity import Entity
from sketch.util.point import Point
import collision
from abc import ABCMeta

class PhysicsEntity(Entity, metaclass=ABCMeta):
  def __init__(
      self,
      velocity:Point=None,
      acceleration:Point=None,
      frozen:bool=False,
      **entity_kwargs
  ):
    Entity.__init__(self, **entity_kwargs)
    def get_or_zero(pt):
      if pt is None:
        return Point(0, 0)
      else:
        return pt
    self.frozen=frozen
    self.velocity = get_or_zero(velocity)
    self.acceleration = get_or_zero(acceleration)
    self._needs_collision_response = True
    # Updated based on collisions
    self._post_collision_dir = Point(0, 0)
    self._post_collision_delta = Point(0, 0)

  def step(self, timestep, scene, audio_sampler):
    Entity.step(self, timestep, scene, audio_sampler)
    if not self.frozen:
      self.move(self.velocity * timestep)
      self.velocity += self.acceleration * timestep

  def pre_collision(self)->None:
    Entity.pre_collision(self)
    self._post_collision_dir = Point(0, 0)
    self._post_collision_delta = Point(0, 0)

  def on_collision(self, other:Entity, response:collision.Response)->None:
    Entity.on_collision(self, other, response)
    self._post_collision_delta -= response.overlap_v
    self._post_collision_dir += response.overlap_n

  def collision_step(self, timestep, scene, audio_sampler)->None:
    Entity.collision_step(self, timestep, scene, audio_sampler)
    if not self.frozen:
      if self._post_collision_dir.magnitude() > 0:
        self.velocity += (
            self.velocity.to_collision_vec()
            .reflect(
              self._post_collision_dir.to_collision_vec()
            )
        )
      self.move(self._post_collision_delta)


class PhysicsCircle(PhysicsEntity):
  def __init__(self, radius:float, **kwargs):
    PhysicsEntity.__init__(self, **kwargs)
    self.radius = radius
    self.collision_shape = collision.Circle(
        collision.Vector(0, 0),
        self.radius
    )

  def draw(self, draw_ctx)->None:
    top_left = self.position - (self.radius, self.radius)
    bot_right = self.position + (self.radius, self.radius)
    draw_ctx.ellipse(
        (top_left.x, top_left.y, bot_right.x, bot_right.y),
        fill=self.color.to8bit_rgba()
    )


def size_to_collision_rect(
    size:Point,
    position:Point=None,
    angle:float=0
)->collision.Poly:
  if position is None:
    position = Point(0, 0)
  bot_left = collision.Vector(-size.x/2, -size.y/2)
  return collision.Poly(
        pos=collision.Vector(position.x, position.y),
        points=[
          bot_left,
          bot_left + Point(0, size.y),
          bot_left + Point(size.x, size.y),
          bot_left + Point(size.x, 0),
        ],
        angle=angle
    )

class PhysicsRectangle(PhysicsEntity):
  def __init__(self, size:Point, **kwargs):
    """
    Note that PhysicsRectangle.position indicates the center
    """
    PhysicsEntity.__init__(self, **kwargs)
    self.size = size
    self.collision_shape = size_to_collision_rect(self.size)

  def draw(self, draw_ctx)->None:
    draw_ctx.polygon(
        [(p.x, p.y) for p in self.collision_shape.points],
        fill=self.color.to8bit_rgba()
    )
