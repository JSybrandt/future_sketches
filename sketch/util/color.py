from random import random

class Color(object):
  def __init__(self, r:float, g:float, b:float, a:float=1):
    domain_err =  "Color values are between 0 and 1"
    assert 0 <= r <= 1, domain_err
    assert 0 <= g <= 1, domain_err
    assert 0 <= b <= 1, domain_err
    assert 0 <= a <= 1, domain_err
    self.r = r
    self.g = g
    self.b = b
    self.a = a

  def __iter__(self):
    yield self.r
    yield self.g
    yield self.b
    yield self.a

  def copy(self):
    return Color(self.r, self.g, self.b, self.a)

  def to8bit_rgba(self):
    return tuple(int(255*x) for x in [self.r, self.g, self.b, self.a])

  @classmethod
  def Random(cls):
    return Color(
        r=random(),
        b=random(),
        g=random(),
        a=1
    )
