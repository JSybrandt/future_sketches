from random import random
import math

class Point:
  def __init__(self, x, y=None):
    if y is None:
      self.x = x[0]
      self.y = x[1]
    else:
      self.x = x
      self.y = y

  def __getitem__(self, idx):
    if idx == 0:
      return self.x
    if idx == 1:
      return self.y
    raise ValueError("Invalid point index")

  def __setitem__(self, idx, val):
    if idx == 0:
      self.x = val
    if idx == 1:
      self.y = val
    raise ValueError("Invalid point index")

  def __iadd__(self, other):
    self.x += other[0]
    self.y += other[1]
    return self

  def __add__(self, other):
    return Point(
      x=self.x+other[0],
      y=self.y+other[1]
    )

  def __isub__(self, other):
    self.x -= other[0]
    self.y -= other[1]
    return self

  def __sub__(self, other):
    return Point(
      x=self.x-other[0],
      y=self.y-other[1]
    )

  def __imul__(self, scale):
    self.x *= scale
    self.y *= scale
    return self

  def __mul__(self, scale):
    return Point(
      x=self.x*scale,
      y=self.y*scale
    )

  def __idiv__(self, scale):
    self.x /= scale
    self.y /= scale
    return self

  def __truediv__(self, scale):
    return Point(
      x=self.x/scale,
      y=self.y/scale
    )

  def length(self):
    return math.sqrt(self.x**2 + self.y**2)

  def unit(self):
    return self / self.length()

  def __str__(self):
    return f"({self.x}, {self.y})"

  def to_int(self):
    return Point(
        x=int(self.x),
        y=int(self.y),
    )

  def copy(self):
    return Point(self.x, self.y)

  def is_positive(self):
    return self.x > 0 and self.y > 0

  def __iter__(self):
    yield self.x
    yield self.y

  def __eq__(self, other):
    return self.x == other[0] and self.y == other[1]

  @classmethod
  def RandomDirection(cls):
    return Point(random()-0.5, random()-0.5).unit()

  @classmethod
  def Random(cls, bounds):
    return Point(
        x=bounds[0]*random(),
        y=bounds[1]*random()
    )

UP = Point(x=0, y=-1)
DOWN = Point(x=0, y=1)
LEFT = Point(x=-1, y=0)
RIGHT = Point(x=1, y=0)
